from django.core.management.base import BaseCommand
from accounts.models import County, Constituency, Ward, PollingStation


class Command(BaseCommand):
    help = "Seed Laikipia County location data (clean + safe + idempotent)"

    def handle(self, *args, **kwargs):

        self.stdout.write("Seeding Laikipia locations...")

        # ================= COUNTY =================
        county, _ = County.objects.get_or_create(name="Laikipia")

        # =====================================================
        # CONSTITUENCIES
        # =====================================================
        east, _ = Constituency.objects.get_or_create(name="Laikipia East", county=county)
        north, _ = Constituency.objects.get_or_create(name="Laikipia North", county=county)
        west, _ = Constituency.objects.get_or_create(name="Laikipia West", county=county)

        # =====================================================
        # ================= LAIKIPIA EAST ====================
        # =====================================================

        nanyuki, _ = Ward.objects.get_or_create(name="Nanyuki Ward", constituency=east)
        tigithi, _ = Ward.objects.get_or_create(name="Tigithi Ward", constituency=east)
        thingithu, _ = Ward.objects.get_or_create(name="Thingithu Ward", constituency=east)
        ngobit, _ = Ward.objects.get_or_create(name="Ngobit Ward", constituency=east)
        umande, _ = Ward.objects.get_or_create(name="Umande Ward", constituency=east)

        PollingStation.objects.get_or_create(name="Nanyuki Primary School", ward=nanyuki)
        PollingStation.objects.get_or_create(name="Likii Market Center", ward=nanyuki)
        PollingStation.objects.get_or_create(name="Nanyuki High School", ward=nanyuki)

        PollingStation.objects.get_or_create(name="Tigithi Market Center", ward=tigithi)
        PollingStation.objects.get_or_create(name="Kiamariga Centre", ward=tigithi)

        PollingStation.objects.get_or_create(name="Thome Community Hall", ward=thingithu)

        # =====================================================
        # ================= LAIKIPIA NORTH ====================
        # =====================================================

        mukogodo_east, _ = Ward.objects.get_or_create(name="Mukogodo East Ward", constituency=north)
        mukogodo_west, _ = Ward.objects.get_or_create(name="Mukogodo West Ward", constituency=north)
        myaka, _ = Ward.objects.get_or_create(name="Segera Ward", constituency=north)
        sosian, _ = Ward.objects.get_or_create(name="Sosian Ward", constituency=north)

        PollingStation.objects.get_or_create(name="Doldol Town Hall", ward=mukogodo_east)
        PollingStation.objects.get_or_create(name="Mukogodo Forest Centre", ward=mukogodo_west)
        PollingStation.objects.get_or_create(name="Olmoran Centre", ward=myaka)
        PollingStation.objects.get_or_create(name="Sosian Ranch Gate", ward=sosian)

        # =====================================================
        # ================= LAIKIPIA WEST =====================
        # =====================================================

        ol_moran, _ = Ward.objects.get_or_create(name="Ol-Moran Ward", constituency=west)
        rumuruti, _ = Ward.objects.get_or_create(name="Rumuruti Township Ward", constituency=west)
        salama, _ = Ward.objects.get_or_create(name="Salama Ward", constituency=west)
        marmanet, _ = Ward.objects.get_or_create(name="Marmanet Ward", constituency=west)
        igwamiti, _ = Ward.objects.get_or_create(name="Igwamiti Ward", constituency=west)
        githiga, _ = Ward.objects.get_or_create(name="Githiga Ward", constituency=west)

        PollingStation.objects.get_or_create(name="Rumuruti Market", ward=rumuruti)
        PollingStation.objects.get_or_create(name="Rumuruti Stadium", ward=rumuruti)

        PollingStation.objects.get_or_create(name="Sipili Market Center", ward=ol_moran)
        PollingStation.objects.get_or_create(name="Igwamiti Shopping Center", ward=igwamiti)

        PollingStation.objects.get_or_create(name="Salama Trading Center", ward=salama)

        self.stdout.write(self.style.SUCCESS("✅ Laikipia location data seeded successfully!"))