from django.urls import reverse, reverse_lazy
from apps.core.utils import generate_password
from django.views import generic
from django.contrib.auth import views
from django.contrib.auth import login
from django.shortcuts import redirect, render
from apps.core.models import User, UserProfile
from apps.org.models import Org
from apps.core.account_activation_email import send_account_activation_mail
from apps.core.token_generator import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponsePermanentRedirect
from django.utils.encoding import force_str
from apps.core.forms import LabStaffCreationForm, CustomAuthenticationForm, CustomOrgRegisterForm, AddOrgUserForm

from config.mixins import access_mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# from xhtml2pdf import pisa



class LandingPageView(LoginRequiredMixin, access_mixins.RedirectLoggedInUserMixin, generic.TemplateView):
    template_name = 'landing_page.html'


class UserRegisterView(generic.CreateView):
    form_class = CustomOrgRegisterForm
    template_name = 'core/register-user.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        org_name = form.cleaned_data.get('org_name')
        org_address = form.cleaned_data.get('org_address')
        org_email = form.cleaned_data.get('org_email')
        org_website_url = form.cleaned_data.get('org_website_url')
        
        org = Org.objects.create(
            org_name=org_name,
            contact = org_email,
            website_url = org_website_url,
            address = org_address
        )
        
        UserProfile.objects.create(
            user = user,
            org = org,
            first_name = first_name,
            last_name = last_name,
            is_org_admin = True
        )
        
        send_account_activation_mail(self.request, user, email = user.email)
        return super(UserRegisterView, self).form_valid(form)  
    
    def get_success_url(self):
        return reverse('core:login')  


class OrgUserAddView(generic.CreateView):
    model = User
    template_name = 'core/add-user.html'
    form_class = AddOrgUserForm
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(str(generate_password()))
        user.save()
        profile = UserProfile.objects.create(
            user = user,
            first_name = user.first_name,
            last_name = user.last_name,
            org = self.request.user.profile.org
        )
        
        # Set the selected role based on the form data
        role = form.cleaned_data['role']
        profile.is_org_admin = (role == 'is_org_admin')
        profile.is_dept_incharge = (role == 'is_dept_incharge')
        profile.is_lab_staff = (role == 'is_lab_staff')

        # Save the profile with the role information
        profile.save()
        
        return super().form_valid(form)

    def get_success_url(self):
        org_id = self.request.user.profile.org.pk
        return reverse('org:org-people-list', kwargs={'org_id':org_id})



class UserDeleteView(generic.DeleteView):
    model = User
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = self.kwargs["user_id"])
        user.delete()
        return HttpResponsePermanentRedirect(reverse('org:org-people-list', kwargs={'org_id':self.request.user.profile.org.pk}))


class LoginView(views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'core/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('landing-page')
    
    
class LogoutView(views.LogoutView):
    template_name = 'core/logout.html'


class ChangePasswordView(views.PasswordChangeView):
    template_name = 'core/change-password.html'
    success_url = reverse_lazy('landing-page')


class ResetPasswordView(views.PasswordResetView):
    email_template_name = 'core/password_reset/password_reset_email.html'
    html_email_template_name = 'core/password_reset/password_reset_email.html'
    subject_template_name = 'core/password_reset/password_reset_subject.txt'
    success_url = reverse_lazy('core:done-password-reset')
    template_name = 'core/password_reset/password_reset_form.html'


class DonePasswordResetView(views.PasswordResetDoneView):
    template_name = 'core/password_reset/password_reset_done.html'


class ConfirmPasswordResetView(views.PasswordResetConfirmView):
    success_url = reverse_lazy('core:complete-password-reset')
    template_name = 'core/password_reset/password_reset_confirm.html'


class CompletePasswordResetView(views.PasswordResetCompleteView):
    template_name = 'core/password_reset/password_reset_complete.html'


class LabStaffCreateView(generic.FormView):
    model = User
    template_name = 'core/lab-staff-create.html'
    form_class = LabStaffCreationForm
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = str(generate_password())
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        org_id = self.kwargs["org_id"]
        org = Org.objects.get(pk=org_id)
        
        user = User.objects.create(
            email=email,
            password=password,
        )
        
        user_profile = UserProfile.objects.create(
            first_name = first_name,
            last_name = last_name,
            user = user,
            org = org,
            is_lab_staff = True
        )
        
        return super().form_valid(form)
        
    def get_success_url(self):
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return reverse('org:lab:lab-create', kwargs={'org_id':org_id, 'dept_id':dept_id})
       

class ActivateAccountView(generic.View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'core/account-verified.html')
        else:
            return render(request, 'core/account-verified.html')
    
    
# class GenerateReportView(generic.View):
#     def get(self, request, org_id):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()

#         userprofile = UserProfile.objects.get(user=request.user)
#         org = userprofile.org
        
#         report = get_report_data(org)
        
#         print(report)

#         # Combine report data
#         report_data = {
#             'organization_name': org.org_name,
#             'lab_count':len(report),
#             'lab_report': report
#         }
        

#         # Render HTML template
#         template_name = 'core/report.html'  # Replace with your actual template name
#         html = render_to_string(template_name, report_data)

#         # Configure xhtml2pdf options (optional)
#         pdf_options = {
#             'page-size': 'A4',  # Set desired page size
#             'encoding': 'utf-8',  # Set encoding for text content
#         }

#         # Generate PDF
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename=report_{org.org_name}.pdf'

#         result = pisa.CreatePDF(html, dest=response, options=pdf_options)
#         if result.err:
#             return HttpResponse('Error: {}'.format(result.err))  # Handle errors

#         return response
    
    
    
# class GenerateLabReportView(generic.View):
#     def get(self, request, org_id, dept_id, lab_id):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()

#         userprofile = UserProfile.objects.get(user=request.user)
#         org = userprofile.org
#         lab = Lab.objects.get(pk = lab_id)
        
#         report = get_lab_report_data(lab)
        

#         # Combine report data
#         report_data = {
#             'organization_name': org.org_name,
#             'lab': report
#         }
        

#         # Render HTML template
#         template_name = 'core/lab-report.html'  # Replace with your actual template name
#         html = render_to_string(template_name, report_data)

#         # Configure xhtml2pdf options (optional)
#         pdf_options = {
#             'page-size': 'A4',  # Set desired page size
#             'encoding': 'utf-8',  # Set encoding for text content
#         }

#         # Generate PDF
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename=report_{org.org_name}.pdf'

#         result = pisa.CreatePDF(html, dest=response, options=pdf_options)
#         if result.err:
#             return HttpResponse('Error: {}'.format(result.err))  # Handle errors

#         return response
    
    
# class GenerateLabItemReportView(generic.View):
#     def get(self, request, org_id, dept_id, lab_id):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()

#         userprofile = UserProfile.objects.get(user=request.user)
#         org = userprofile.org
#         lab = Lab.objects.get(pk = lab_id)
        
#         report = get_lab_item_report_data(lab)
        

#         # Combine report data
#         report_data = {
#             'organization_name': org.org_name,
#             'lab': report
#         }
        

#         # Render HTML template
#         template_name = 'core/lab-report.html'  # Replace with your actual template name
#         html = render_to_string(template_name, report_data)

#         # Configure xhtml2pdf options (optional)
#         pdf_options = {
#             'page-size': 'A4',  # Set desired page size
#             'encoding': 'utf-8',  # Set encoding for text content
#         }

#         # Generate PDF
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename=report_{org.org_name}.pdf'

#         result = pisa.CreatePDF(html, dest=response, options=pdf_options)
#         if result.err:
#             return HttpResponse('Error: {}'.format(result.err))  # Handle errors

#         return response
    

# class GenerateLabSystemReportView(generic.View):
#     def get(self, request, org_id, dept_id, lab_id):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()

#         userprofile = UserProfile.objects.get(user=request.user)
#         org = userprofile.org
#         lab = Lab.objects.get(pk = lab_id)
        
#         report = get_lab_system_report_data(lab)
        

#         # Combine report data
#         report_data = {
#             'organization_name': org.org_name,
#             'lab': report
#         }
        

#         # Render HTML template
#         template_name = 'core/lab-report.html'  # Replace with your actual template name
#         html = render_to_string(template_name, report_data)

#         # Configure xhtml2pdf options (optional)
#         pdf_options = {
#             'page-size': 'A4',  # Set desired page size
#             'encoding': 'utf-8',  # Set encoding for text content
#         }

#         # Generate PDF
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename=report_{org.org_name}.pdf'

#         result = pisa.CreatePDF(html, dest=response, options=pdf_options)
#         if result.err:
#             return HttpResponse('Error: {}'.format(result.err))  # Handle errors

#         return response