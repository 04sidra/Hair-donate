from django.contrib import admin
from .models import HairDonor, HairRequest, DonationMatch, ContactMessage, UserProfile

@admin.register(HairDonor)
class HairDonorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'city', 'hair_length', 'hair_color', 'status', 'created_at']
    list_filter = ['status', 'gender', 'hair_type', 'hair_color', 'city', 'state']
    search_fields = ['full_name', 'email', 'phone', 'city']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'full_name', 'email', 'phone', 'age', 'gender')
        }),
        ('Address Details', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Hair Details', {
            'fields': ('hair_length', 'hair_type', 'hair_color', 'hair_condition')
        }),
        ('Donation Status', {
            'fields': ('willing_to_donate', 'donation_date', 'status')
        }),
    )


@admin.register(HairRequest)
class HairRequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'patient_type', 'urgency', 'city', 'request_status', 'created_at']
    list_filter = ['request_status', 'patient_type', 'urgency', 'city', 'state']
    search_fields = ['patient_name', 'email', 'phone', 'hospital_name']
    list_editable = ['request_status']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('user', 'patient_name', 'email', 'phone', 'age')
        }),
        ('Address Details', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Medical Details', {
            'fields': ('patient_type', 'medical_condition', 'urgency', 'medical_certificate')
        }),
        ('Hair Requirements', {
            'fields': ('required_hair_length', 'preferred_hair_color', 'preferred_hair_type')
        }),
        ('Hospital Information', {
            'fields': ('hospital_name', 'doctor_name', 'doctor_contact')
        }),
        ('Request Management', {
            'fields': ('request_status', 'matched_donor', 'admin_notes')
        }),
    )


@admin.register(DonationMatch)
class DonationMatchAdmin(admin.ModelAdmin):
    list_display = ['donor', 'request', 'matched_date', 'donation_completed', 'completion_date']
    list_filter = ['donation_completed', 'matched_date']
    search_fields = ['donor__full_name', 'request__patient_name']
    date_hierarchy = 'matched_date'
    
    fieldsets = (
        ('Match Details', {
            'fields': ('donor', 'request', 'matched_date')
        }),
        ('Completion Status', {
            'fields': ('donation_completed', 'completion_date', 'feedback', 'rating')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']