from django.core.management.base import BaseCommand
from accounts.models import County, Constituency, Ward, PollingStation


class Command(BaseCommand):
    help = "Seed Laikipia County location data (clean + idempotent)"

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
        # LAIKIPIA EAST WARDS
        # =====================================================
        wards_east = [
            "Ngobit Ward",
            "Tigithi Ward",
            "Thingithu Ward",
            "Nanyuki Ward",
            "Umande Ward",
        ]

        east_wards = {}
        for w in wards_east:
            obj, _ = Ward.objects.get_or_create(name=w, constituency=east)
            east_wards[w] = obj

        # =====================================================
        # LAIKIPIA NORTH WARDS
        # =====================================================
        wards_north = [
            "Mukogodo East Ward",
            "Mukogodo West Ward",
            "Segera Ward",
            "Sosian Ward",
        ]

        north_wards = {}
        for w in wards_north:
            obj, _ = Ward.objects.get_or_create(name=w, constituency=north)
            north_wards[w] = obj

        # =====================================================
        # LAIKIPIA WEST WARDS
        # =====================================================
        wards_west = [
            "Ol-Moran Ward",
            "Rumuruti Township Ward",
            "Salama Ward",
            "Marmanet Ward",
            "Igwamiti Ward",
            "Githiga Ward",
        ]

        west_wards = {}
        for w in wards_west:
            obj, _ = Ward.objects.get_or_create(name=w, constituency=west)
            west_wards[w] = obj

        # =====================================================
        # POLLING STATIONS (CLEAN STRUCTURE)
        # =====================================================

        # EAST
        PollingStation.objects.get_or_create(name="Nanyuki Primary School", ward=east_wards["Nanyuki Ward"])
        PollingStation.objects.get_or_create(name="Likii Market Center", ward=east_wards["Nanyuki Ward"])
        PollingStation.objects.get_or_create(name="Nanyuki High School", ward=east_wards["Nanyuki Ward"])

        PollingStation.objects.get_or_create(name="Tigithi Market Center", ward=east_wards["Tigithi Ward"])
        PollingStation.objects.get_or_create(name="Kiamariga Centre", ward=east_wards["Tigithi Ward"])

        PollingStation.objects.get_or_create(name="Thome Community Hall", ward=east_wards["Thingithu Ward"])

        # NORTH
        PollingStation.objects.get_or_create(name="Doldol Town Hall", ward=north_wards["Mukogodo East Ward"])
        PollingStation.objects.get_or_create(name="Mukogodo Forest Centre", ward=north_wards["Mukogodo West Ward"])

        PollingStation.objects.get_or_create(name="Olmoran Centre", ward=north_wards["Segera Ward"])
        PollingStation.objects.get_or_create(name="Sosian Ranch Gate", ward=north_wards["Sosian Ward"])

        # WEST
        PollingStation.objects.get_or_create(name="Rumuruti Market", ward=west_wards["Rumuruti Township Ward"])
        PollingStation.objects.get_or_create(name="Rumuruti Stadium", ward=west_wards["Rumuruti Township Ward"])

        PollingStation.objects.get_or_create(name="Sipili Market Center", ward=west_wards["Ol-Moran Ward"])
        PollingStation.objects.get_or_create(name="Igwamiti Shopping Center", ward=west_wards["Igwamiti Ward"])

        PollingStation.objects.get_or_create(name="Salama Trading Center", ward=west_wards["Salama Ward"])

        self.stdout.write(self.style.SUCCESS("✅ Laikipia location data seeded successfully!"))