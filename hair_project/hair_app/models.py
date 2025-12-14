from django.db import models
from django.contrib.auth.models import User

class HairDonor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    HAIR_TYPE_CHOICES = [
        ('Straight', 'Straight'),
        ('Wavy', 'Wavy'),
        ('Curly', 'Curly'),
        ('Coily', 'Coily'),
    ]
    
    HAIR_COLOR_CHOICES = [
        ('Black', 'Black'),
        ('Brown', 'Brown'),
        ('Blonde', 'Blonde'),
        ('Red', 'Red'),
        ('Grey', 'Grey'),
        ('Other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Donated', 'Donated'),
        ('Pending', 'Pending'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    hair_length = models.FloatField(help_text="Hair length in inches")
    hair_type = models.CharField(max_length=20, choices=HAIR_TYPE_CHOICES)
    hair_color = models.CharField(max_length=20, choices=HAIR_COLOR_CHOICES)
    hair_condition = models.TextField(help_text="Any chemical treatments, dyed, etc.")
    
    willing_to_donate = models.BooleanField(default=True)
    donation_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.hair_length} inches"
    
    class Meta:
        ordering = ['-created_at']


class HairRequest(models.Model):
    PATIENT_TYPE_CHOICES = [
        ('Cancer', 'Cancer Patient'),
        ('Burn', 'Burn Victim'),
        ('Alopecia', 'Alopecia'),
        ('Medical', 'Medical Treatment'),
        ('Other', 'Other'),
    ]
    
    URGENCY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Emergency', 'Emergency'),
    ]
    
    REQUEST_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Matched', 'Matched with Donor'),
        ('Fulfilled', 'Fulfilled'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    patient_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    patient_type = models.CharField(max_length=20, choices=PATIENT_TYPE_CHOICES)
    medical_condition = models.TextField(help_text="Brief description of medical condition")
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES)
    
    required_hair_length = models.FloatField(help_text="Minimum hair length needed in inches")
    preferred_hair_color = models.CharField(max_length=100, blank=True)
    preferred_hair_type = models.CharField(max_length=100, blank=True)
    
    hospital_name = models.CharField(max_length=200, blank=True)
    doctor_name = models.CharField(max_length=200, blank=True)
    doctor_contact = models.CharField(max_length=15, blank=True)
    medical_certificate = models.FileField(upload_to='medical_certificates/', null=True, blank=True)
    
    request_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='Pending')
    matched_donor = models.ForeignKey(HairDonor, on_delete=models.SET_NULL, null=True, blank=True)
    
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient_name} - {self.patient_type} - {self.urgency}"
    
    class Meta:
        ordering = ['-urgency', '-created_at']


class DonationMatch(models.Model):
    donor = models.ForeignKey(HairDonor, on_delete=models.CASCADE)
    request = models.ForeignKey(HairRequest, on_delete=models.CASCADE)
    matched_date = models.DateTimeField(auto_now_add=True)
    donation_completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True, help_text="Rating from 1-5")
    
    def __str__(self):
        return f"{self.donor.full_name} -> {self.request.patient_name}"
    
    class Meta:
        ordering = ['-matched_date']


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"