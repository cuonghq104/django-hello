from django.db import models

from api.models import User


class Store(models.Model):
    class LocationChoice(models.TextChoices):
        HA_NOI = "HN",
        HUE = "HUE",
        HAI_PHONG = "HP",
        DA_NANG = "DN",
        CAN_THO = "CT",
        HO_CHI_MINH = "HCM",
        CAO_BANG = "CB",
        LANG_SON = "LS",
        LAI_CHAU = "LC",
        DIEN_BIEN = "DB",
        SON_LA = "SL",
        THANH_HOA = "TH",
        NGHE_AN = "NA",
        HA_TINH = "HT",
        QUANG_NINH = "QN",
        TUYEN_QUANG = "TQ",
        LAO_CAI = "LCI",
        THAI_NGUYEN = "TN",
        PHU_THO = "PT",
        BAC_NINH = "BN",
        HUNG_YEN = "HY",
        NINH_BINH = "NB",
        QUANG_TRI = "QT",
        QUANG_NGAI = "QNG",
        GIA_LAI = "GL",
        KHANH_HOA = "KH",
        LAM_DONG = "LD",
        DAK_LAK = "DK",
        DONG_NAI = "DNAI",
        TAY_NINH = "TNIN",
        VINH_LONG = "VL",
        DONG_THAP = "DT",
        CA_MAU = "CM",
        AN_GIANG = "AG",

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    location = models.CharField(max_length=100, choices=LocationChoice.choices, default=LocationChoice.HA_NOI)

    def __str__(self):
        return self.name

class StoreStaff(models.Model):
    class RoleChoice(models.TextChoices):
        OWNER = "1",  "Owner",
        EMPLOYER = "2", "Employee",

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_stores')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='staff_users')
    role = models.CharField(choices=RoleChoice.choices, default=RoleChoice.OWNER, max_length=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'store')

    def __str__(self):
        return f"{self.user.username} - {self.role}"