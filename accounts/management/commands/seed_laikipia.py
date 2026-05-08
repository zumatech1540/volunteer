from django.core.management.base import BaseCommand
from accounts.models import County, Constituency, Ward, PollingStation


class Command(BaseCommand):
    help = "Seed Laikipia County location data (safe + idempotent)"

    def handle(self, *args, **kwargs):

        # ================= COUNTY =================
        county, _ = County.objects.get_or_create(name="Laikipia")

        # ================= CONSTITUENCIES =================
        east, _ = Constituency.objects.get_or_create(name="Laikipia East", county=county)
        north, _ = Constituency.objects.get_or_create(name="Laikipia North", county=county)
        west, _ = Constituency.objects.get_or_create(name="Laikipia West", county=county)

        # =========================================================
        # EAST
        # =========================================================
        nanyuki, _ = Ward.objects.get_or_create(name="Nanyuki", constituency=east)
        tigithi, _ = Ward.objects.get_or_create(name="Tigithi", constituency=east)
        thome, _ = Ward.objects.get_or_create(name="Thome", constituency=east)
        sosian_east, _ = Ward.objects.get_or_create(name="Sosian East", constituency=east)

        # =========================================================
        # NORTH
        # =========================================================
        doldol, _ = Ward.objects.get_or_create(name="Doldol", constituency=north)
        mairungi, _ = Ward.objects.get_or_create(name="Mairungi", constituency=north)
        mukogodo, _ = Ward.objects.get_or_create(name="Mukogodo", constituency=north)
        ilgwesi, _ = Ward.objects.get_or_create(name="Ilgwesi", constituency=north)

        # =========================================================
        # WEST
        # =========================================================
        rumuruti, _ = Ward.objects.get_or_create(name="Rumuruti", constituency=west)
        sipili, _ = Ward.objects.get_or_create(name="Sipili", constituency=west)
        igwamiti, _ = Ward.objects.get_or_create(name="Igwamiti", constituency=west)
        salama, _ = Ward.objects.get_or_create(name="Salama", constituency=west)

        # =========================================================
        # POLLING STATIONS (EAST)
        # =========================================================
        PollingStation.objects.get_or_create(name="Nanyuki Primary School", ward=nanyuki)
        PollingStation.objects.get_or_create(name="Likii Market Center", ward=nanyuki)
        PollingStation.objects.get_or_create(name="Nanyuki High School", ward=nanyuki)

        PollingStation.objects.get_or_create(name="Tigithi Market Center", ward=tigithi)
        PollingStation.objects.get_or_create(name="Kiamariga Centre", ward=tigithi)

        PollingStation.objects.get_or_create(name="Thome Community Hall", ward=thome)

        PollingStation.objects.get_or_create(name="Sosian Ranch Gate", ward=sosian_east)

        # =========================================================
        # POLLING STATIONS (NORTH)
        # =========================================================
        PollingStation.objects.get_or_create(name="Doldol Town Hall", ward=doldol)
        PollingStation.objects.get_or_create(name="Olmoran Centre", ward=doldol)

        PollingStation.objects.get_or_create(name="Mairungi Primary School", ward=mairungi)
        PollingStation.objects.get_or_create(name="Mukogodo Forest Centre", ward=mukogodo)

        PollingStation.objects.get_or_create(name="Ilgwesi Trading Center", ward=ilgwesi)

        # =========================================================
        # POLLING STATIONS (WEST)
        # =========================================================
        PollingStation.objects.get_or_create(name="Rumuruti Market", ward=rumuruti)
        PollingStation.objects.get_or_create(name="Rumuruti Stadium", ward=rumuruti)

        PollingStation.objects.get_or_create(name="Sipili Market Center", ward=sipili)
        PollingStation.objects.get_or_create(name="Igwamiti Shopping Center", ward=igwamiti)

        PollingStation.objects.get_or_create(name="Salama Trading Center", ward=salama)

        self.stdout.write(self.style.SUCCESS("✅ Laikipia location data seeded successfully!"))