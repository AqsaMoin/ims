from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView, CreateView, View
from inventory.models import Category, Purchase, Room, Brand, Item, System, SystemComponent, Issue, ItemGroup, ItemGroupItem, RoomSettings  # Import RoomSettings
from inventory.forms.room_incharge import CategoryForm, BrandForm, ItemForm, ItemPurchaseForm, PurchaseForm, PurchaseUpdateForm, SystemForm, SystemComponentForm, ItemGroupForm, ItemGroupItemForm, RoomSettingsForm  # Import RoomSettingsForm
from django.contrib import messages
from django.views.generic.edit import FormView
from inventory.forms.room_incharge import SystemComponentArchiveForm, ItemArchiveForm, RoomUpdateForm
from inventory.models import Archive
from inventory.forms.room_incharge import PurchaseCompleteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/category_list.html'
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'room_incharge/category_update.html'
    form_class = CategoryForm
    success_url = reverse_lazy('room_incharge:category_list')
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:category_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.profile.org
        category.room = Room.objects.get(slug=self.kwargs['room_slug'])
        category.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'room_incharge/category_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:category_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'room_incharge/category_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('room_incharge:category_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:category_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.profile.org
        category.room = Room.objects.get(slug=self.kwargs['room_slug'])
        category.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['room'] = Room.objects.get(slug=self.kwargs['room_slug'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class RoomDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'room_incharge/room_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_slug = self.kwargs['room_slug']
        room = Room.objects.get(slug=room_slug)
        context['room'] = room
        context['room_slug'] = room_slug
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    template_name = 'room_incharge/room_update.html'
    form_class = RoomUpdateForm
    slug_field = 'slug'
    slug_url_kwarg = 'room_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:room_dashboard', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        room = form.save(commit=False)
        room.organisation = self.request.user.profile.org
        room.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class BrandListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/brand_list.html'
    model = Brand
    context_object_name = 'brands'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    template_name = 'room_incharge/brand_create.html'
    form_class = BrandForm
    success_url = reverse_lazy('room_incharge:brand_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:brand_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        brand = form.save(commit=False)
        brand.organisation = self.request.user.profile.org
        brand.room = Room.objects.get(slug=self.kwargs['room_slug'])
        brand.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['room'] = Room.objects.get(slug=self.kwargs['room_slug'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class BrandUpdateView(LoginRequiredMixin, UpdateView):
    model = Brand
    template_name = 'room_incharge/brand_update.html'
    form_class = BrandForm
    success_url = reverse_lazy('room_incharge:brand_list')
    slug_field = 'slug'
    slug_url_kwarg = 'brand_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:brand_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        brand = form.save(commit=False)
        brand.organisation = self.request.user.profile.org
        brand.room = Room.objects.get(slug=self.kwargs['room_slug'])
        brand.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class BrandDeleteView(LoginRequiredMixin, DeleteView):
    model = Brand
    template_name = 'room_incharge/brand_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'brand_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:brand_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/item_list.html'
    model = Item
    context_object_name = 'items'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'room_incharge/item_create.html'
    form_class = ItemForm
    success_url = reverse_lazy('room_incharge:item_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        item = form.save(commit=False)
        item.organisation = self.request.user.profile.org
        item.room = Room.objects.get(slug=self.kwargs['room_slug'])
        item.achived_count = 0  # Set default value
        item.available_count = item.total_count  # Set available_count to total_count
        item.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['room'] = Room.objects.get(slug=self.kwargs['room_slug'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'room_incharge/item_update.html'
    form_class = ItemForm
    success_url = reverse_lazy('room_incharge:item_list')
    slug_field = 'slug'
    slug_url_kwarg = 'item_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        item = form.save(commit=False)
        item.organisation = self.request.user.profile.org
        item.room = Room.objects.get(slug=self.kwargs['room_slug'])
        item.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'room_incharge/item_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'item_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemArchiveView(LoginRequiredMixin, FormView):
    template_name = 'room_incharge/item_archive.html'
    form_class = ItemArchiveForm
    success_url = reverse_lazy('room_incharge:item_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        item = Item.objects.get(slug=self.kwargs['item_slug'])
        count = form.cleaned_data['count']

        if item.available_count < count:
            form.add_error('count', 'The count provided exceeds the available count.')
            return self.form_invalid(form)

        # Create an archive entry
        Archive.objects.create(
            organisation=item.organisation,
            department=item.department,
            room=item.room,
            item=item,
            count=count,
            archive_type=form.cleaned_data['archive_type'],
            remark=form.cleaned_data['remark']
        )

        # Update item counts
        item.available_count -= count
        item.achived_count += count
        item.save()

        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['item_slug'] = self.kwargs['item_slug']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class SystemListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/system_list.html'
    model = System
    context_object_name = 'systems'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class SystemCreateView(LoginRequiredMixin, CreateView):
    model = System
    template_name = 'room_incharge/system_create.html'
    form_class = SystemForm
    success_url = reverse_lazy('room_incharge:system_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:system_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        system = form.save(commit=False)
        system.organisation = self.request.user.profile.org
        system.room = Room.objects.get(slug=self.kwargs['room_slug'])
        system.department = system.room.department  # Set the department field
        system.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['room'] = Room.objects.get(slug=self.kwargs['room_slug'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class SystemUpdateView(LoginRequiredMixin, UpdateView):
    model = System
    template_name = 'room_incharge/system_update.html'
    form_class = SystemForm
    success_url = reverse_lazy('room_incharge:system_list')
    slug_field = 'slug'
    slug_url_kwarg = 'system_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:system_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        system = form.save(commit=False)
        system.organisation = self.request.user.profile.org
        system.room = Room.objects.get(slug=self.kwargs['room_slug'])
        system.department = system.room.department  # Set the department field
        system.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class SystemDeleteView(LoginRequiredMixin, DeleteView):
    model = System
    template_name = 'room_incharge/system_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'system_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:system_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class SystemComponentListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/system_component_list.html'
    model = SystemComponent
    context_object_name = 'components'

    def get_queryset(self):
        system_slug = self.kwargs['system_slug']
        return super().get_queryset().filter(system__slug=system_slug, system__organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system_slug'] = self.kwargs['system_slug']
        context['room_slug'] = self.kwargs['room_slug']
        context['system'] = get_object_or_404(System, slug=self.kwargs['system_slug'])
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class SystemComponentCreateView(LoginRequiredMixin, CreateView):
    model = SystemComponent
    template_name = 'room_incharge/system_component_create.html'
    form_class = SystemComponentForm
    success_url = reverse_lazy('room_incharge:system_component_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:system_component_list', kwargs={'room_slug': self.kwargs['room_slug'], 'system_slug': self.kwargs['system_slug']})

    def form_valid(self, form):
        component = form.save(commit=False)
        component.system = System.objects.get(slug=self.kwargs['system_slug'])
        try:
            component.save()
        except ValueError as e:
            form.add_error(None, str(e))
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        
        # Adjust the available_count and in_use count of the associated Item
        item = component.component_item
        item.available_count -= 1
        item.in_use += 1
        item.save()
        
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['system'] = System.objects.get(slug=self.kwargs['system_slug'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system_slug'] = self.kwargs['system_slug']
        context['room_slug'] = self.kwargs['room_slug']
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class SystemComponentUpdateView(LoginRequiredMixin, UpdateView):
    model = SystemComponent
    template_name = 'room_incharge/system_component_update.html'
    form_class = SystemComponentForm
    success_url = reverse_lazy('room_incharge:system_component_list')
    slug_field = 'slug'
    slug_url_kwarg = 'component_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:system_component_list', kwargs={'room_slug': self.kwargs['room_slug'], 'system_slug': self.kwargs['system_slug']})

    def form_valid(self, form):
        component = form.save(commit=False)
        component.system = System.objects.get(slug=self.kwargs['system_slug'])
        
        # Get the old component item before saving the new one
        old_component = SystemComponent.objects.get(pk=component.pk)
        old_item = old_component.component_item
        
        try:
            component.save()
        except ValueError as e:
            form.add_error(None, str(e))
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        
        # Adjust the counts if the item has changed
        new_item = component.component_item
        if old_item != new_item:
            old_item.available_count += 1
            old_item.in_use -= 1
            old_item.save()
            
            new_item.available_count -= 1
            new_item.in_use += 1
            new_item.save()
        
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system_slug'] = self.kwargs['system_slug']
        context['room_slug'] = self.kwargs['room_slug']
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class SystemComponentDeleteView(LoginRequiredMixin, DeleteView):
    model = SystemComponent
    template_name = 'room_incharge/system_component_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'component_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:system_component_list', kwargs={'room_slug': self.kwargs['room_slug'], 'system_slug': self.kwargs['system_slug']})

    def get_queryset(self):
        system_slug = self.kwargs['system_slug']
        return super().get_queryset().filter(system__slug=system_slug, system__organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system_slug'] = self.kwargs['system_slug']
        context['room_slug'] = self.kwargs['room_slug']
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class SystemComponentArchiveView(LoginRequiredMixin, FormView):
    template_name = 'room_incharge/system_component_archive.html'
    form_class = SystemComponentArchiveForm
    success_url = reverse_lazy('room_incharge:system_component_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:system_component_list', kwargs={'room_slug': self.kwargs['room_slug'], 'system_slug': self.kwargs['system_slug']})

    def form_valid(self, form):
        component = SystemComponent.objects.get(slug=self.kwargs['component_slug'])
        item = component.component_item

        # Create an archive entry
        Archive.objects.create(
            organisation=item.organisation,
            department=item.department,
            room=item.room,
            item=item,
            count=1,
            archive_type=form.cleaned_data['archive_type'],
            remark=form.cleaned_data['remark']
        )

        # Update item counts
        item.in_use -= 1
        item.achived_count += 1
        item.save()

        # Delete the system component
        component.delete()

        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['component_slug'] = self.kwargs['component_slug']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system_slug'] = self.kwargs['system_slug']
        context['room_slug'] = self.kwargs['room_slug']
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ArchiveListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/archive_list.html'
    model = Archive
    context_object_name = 'archives'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class PurchaseListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/purchase_list.html'
    model = Purchase
    context_object_name = 'purchases'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = 'room_incharge/purchase_create.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('room_incharge:purchase_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:purchase_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        purchase = form.save(commit=False)
        purchase.organisation = self.request.user.profile.org
        purchase.room = Room.objects.get(slug=self.kwargs['room_slug'])
        purchase.status = 'requested'  # Set default status to requested
        purchase.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Purchase
    template_name = 'room_incharge/purchase_update.html'
    form_class = PurchaseUpdateForm
    success_url = reverse_lazy('room_incharge:purchase_list')
    slug_field = 'slug'
    slug_url_kwarg = 'purchase_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:purchase_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        purchase = form.save(commit=False)
        if purchase.status != 'requested':
            purchase.status = 'requested'  # Set status to requested if not already
        purchase.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class PurchaseNewItemCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = 'room_incharge/purchase_new_item_create.html'
    form_class = ItemPurchaseForm
    success_url = reverse_lazy('room_incharge:purchase_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:purchase_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        item = Item.objects.create(
            organisation=self.request.user.profile.org,
            department=room.department,  # Set department from the associated room
            room=room,
            category=form.cleaned_data['category'],
            brand=form.cleaned_data['brand'],
            item_name=form.cleaned_data['item_name'],
            total_count=0,  # Set initial total_count to 0
            available_count=0,  # Set initial available_count to 0
            is_listed=False
        )
        purchase = form.save(commit=False)
        purchase.organisation = self.request.user.profile.org
        purchase.room = room
        purchase.item = item
        purchase.status = 'requested'  # Set default status to requested
        purchase.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = 'room_incharge/purchase_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'purchase_slug'
    success_url = reverse_lazy('room_incharge:purchase_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:purchase_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class PurchaseCompleteView(LoginRequiredMixin, FormView):
    template_name = 'room_incharge/purchase_complete.html'
    form_class = PurchaseCompleteForm
    success_url = reverse_lazy('room_incharge:purchase_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:purchase_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        purchase = Purchase.objects.get(slug=self.kwargs['purchase_slug'])
        receipt = form.save(commit=False)
        receipt.purchase = purchase
        receipt.org = self.request.user.profile.org
        receipt.save()
        purchase.status = 'completed'
        purchase.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['purchase_slug'] = self.kwargs['purchase_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class PurchaseAddToStockView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        purchase = get_object_or_404(Purchase, slug=self.kwargs['purchase_slug'])
        if purchase.status == 'completed' and not purchase.added_to_stock:
            item = purchase.item
            item.total_count += purchase.quantity
            item.available_count += purchase.quantity
            if not item.is_listed:
                item.is_listed = True
            item.save()
            purchase.added_to_stock = True
            purchase.save()
            messages.success(request, f"Added {purchase.quantity} {purchase.unit_of_measure} to {item.item_name} stock.")
        return redirect('room_incharge:purchase_list', room_slug=self.kwargs['room_slug'])

class IssueListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/issue_list.html'
    model = Issue
    context_object_name = 'issues'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemGroupListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/item_group_list.html'
    model = ItemGroup
    context_object_name = 'item_groups'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemGroupCreateView(LoginRequiredMixin, CreateView):
    model = ItemGroup
    template_name = 'room_incharge/item_group_create.html'
    form_class = ItemGroupForm
    success_url = reverse_lazy('room_incharge:item_group_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_group_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        item_group = form.save(commit=False)
        item_group.organisation = self.request.user.profile.org
        item_group.room = Room.objects.get(slug=self.kwargs['room_slug'])
        item_group.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemGroupItemCreateView(LoginRequiredMixin, CreateView):
    model = ItemGroupItem
    template_name = 'room_incharge/item_group_item_create.html'
    form_class = ItemGroupItemForm

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_group_item_list', kwargs={'room_slug': self.kwargs['room_slug'], 'item_group_slug': self.kwargs['item_group_slug']})

    def form_valid(self, form):
        item_group_item = form.save(commit=False)
        item_group_item.item_group = ItemGroup.objects.get(slug=self.kwargs['item_group_slug'])
        item = item_group_item.item

        # Adjust the available_count and in_use count of the associated Item
        item.available_count -= item_group_item.qty
        item.in_use += item_group_item.qty

        try:
            item_group_item.save()
            item.save()
        except ValueError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_slug'] = self.kwargs['room_slug']
        context['item_group_slug'] = self.kwargs['item_group_slug']
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemGroupItemListView(LoginRequiredMixin, ListView):
    template_name = 'room_incharge/item_group_item_list.html'
    model = ItemGroupItem
    context_object_name = 'item_group_items'

    def get_queryset(self):
        item_group_slug = self.kwargs['item_group_slug']
        return super().get_queryset().filter(item_group__slug=item_group_slug, item_group__organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_slug'] = self.kwargs['room_slug']
        context['item_group_slug'] = self.kwargs['item_group_slug']
        context['item_group'] = get_object_or_404(ItemGroup, slug=self.kwargs['item_group_slug'])
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ItemGroup
    template_name = 'room_incharge/item_group_update.html'
    form_class = ItemGroupForm
    success_url = reverse_lazy('room_incharge:item_group_list')
    slug_field = 'slug'
    slug_url_kwarg = 'item_group_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_group_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        item_group = form.save(commit=False)
        item_group.organisation = self.request.user.profile.org
        item_group.room = Room.objects.get(slug=self.kwargs['room_slug'])
        item_group.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = ItemGroup
    template_name = 'room_incharge/item_group_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'item_group_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_group_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_slug'] = self.kwargs['room_slug']
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class ItemGroupItemUpdateView(LoginRequiredMixin, UpdateView):
    model = ItemGroupItem
    template_name = 'room_incharge/item_group_item_update.html'
    form_class = ItemGroupItemForm
    slug_field = 'slug'
    slug_url_kwarg = 'item_group_item_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_group_item_list', kwargs={'room_slug': self.kwargs['room_slug'], 'item_group_slug': self.kwargs['item_group_slug']})

    def form_valid(self, form):
        item_group_item = form.save(commit=False)
        item = item_group_item.item
        old_qty = ItemGroupItem.objects.get(pk=item_group_item.pk).qty

        # Adjust the available_count and in_use count of the associated Item
        item.available_count += old_qty - item_group_item.qty
        item.in_use -= old_qty - item_group_item.qty
        item.save()

        item_group_item.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_slug'] = self.kwargs['room_slug']
        context['item_group_slug'] = self.kwargs['item_group_slug']
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context


class ItemGroupItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ItemGroupItem
    template_name = 'room_incharge/item_group_item_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'item_group_item_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:item_group_item_list', kwargs={'room_slug': self.kwargs['room_slug'], 'item_group_slug': self.kwargs['item_group_slug']})

    def get_queryset(self):
        return super().get_queryset().filter(item_group__slug=self.kwargs['item_group_slug'], item_group__organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_slug'] = self.kwargs['room_slug']
        context['item_group_slug'] = self.kwargs['item_group_slug']
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class RoomSettingsView(LoginRequiredMixin, UpdateView):
    model = RoomSettings
    template_name = 'room_incharge/room_settings.html'
    form_class = RoomSettingsForm
    success_url = reverse_lazy('room_incharge:room_dashboard')

    def get_object(self):
        room = get_object_or_404(Room, slug=self.kwargs['room_slug'])
        return RoomSettings.objects.get_or_create(room=room)[0]

    def get_success_url(self):
        return reverse_lazy('room_incharge:room_settings', kwargs={'room_slug': self.kwargs['room_slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_slug'] = self.kwargs['room_slug']
        room = Room.objects.get(slug=self.kwargs['room_slug'])
        context['room_settings'] = RoomSettings.objects.get_or_create(room=room)[0]
        return context

class RoomReportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        room_slug = self.kwargs['room_slug']
        room = get_object_or_404(Room, slug=room_slug)
        room_settings = RoomSettings.objects.get_or_create(room=room)[0]

        context = {
            'room': room,
            'room_settings': room_settings,
            'categories': Category.objects.filter(room=room) if room_settings.categories_tab else None,
            'brands': Brand.objects.filter(room=room) if room_settings.brands_tab else None,
            'items': Item.objects.filter(room=room) if room_settings.items_tab else None,
            'systems': System.objects.filter(room=room) if room_settings.systems_tab else None,
            'item_groups': ItemGroup.objects.filter(room=room) if room_settings.item_groups_tab else None,
            'system_components': SystemComponent.objects.filter(system__room=room) if room_settings.systems_tab else None,
            'purchases': Purchase.objects.filter(room=room),
            'archives': Archive.objects.filter(room=room),
            'issues': Issue.objects.filter(room=room),
        }

        html_string = render_to_string('room_incharge/room_report.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{room.room_name}_report.pdf"'
        return response