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
        githiga, _ = Ward.objects.get_or_create(name="Githiga Ward", constituency=west)
        marmanet, _ = Ward.objects.get_or_create(name="Marmanet Ward", constituency=west)
        igwamiti, _ = Ward.objects.get_or_create(name="Igwamiti Ward", constituency=west)
        salama, _ = Ward.objects.get_or_create(name="Salama Ward", constituency=west)

        # ================= OL-MORAN =================
        for name in [
            "Miharati Primary School",
            "Olmoran Day Secondary School",
            "Laikipia Ranching Primary School",
            "Kabati Primary School",
            "Lariak Primary School",
            "Wangwachi Primary School",
            "Sipili Primary School",
            "Naiborom Primary School",
            "Makutano Nursery School",
            "Dimkom Nursery School",
            "Mahiga Primary School",
            "Kio Primary School",
        ]:
            PollingStation.objects.get_or_create(name=name, ward=ol_moran)

        # ================= RUMURUTI TOWNSHIP =================
        for name in [
            "Rumuruti Primary School",
            "Mutamaiyu Primary School",
            "Manyatta Primary School",
            "Ndurumo Primary School",
            "Mategithi Primary School",
            "Kagaa Primary School",
            "Mwireri Primary School",
            "Machunguru Primary School",
            "Simotwo Primary School",
            "Kapkures Primary School",
            "Ainapmoi Primary School",
            "Magomano Primary School",
            "Ol-Arinyiro Primary School",
            "Othaya OMC Primary School",
            "Mathuri Nursery School",
            "Maji Mengi Nursery School",
            "Samoei Primary School",
            "Emgwen Mixed Day Secondary School",
            "GG Rumuruti Boys Secondary School",
        ]:
            PollingStation.objects.get_or_create(name=name, ward=rumuruti)

        # ================= GITHIGA =================
        for name in [
            "Kinamba Primary School",
            "Kariaini Primary School",
            "Ng'elesha Primary School",
            "Ol Arabel Primary School",
            "Nyakinyua Primary School",
            "Lobere Primary School",
            "Tandare Primary School",
            "Miteta Primary School",
            "Njorua Primary School",
            "Mahua Primary School",
            "Nyakiambi Primary School",
            "Bustani Primary School",
            "Milimani Primary School",
            "Kiwanja Primary School",
            "Ndindika Primary School",
            "G.G. Kinamba High School",
            "Kisima Primary School",
            "Mbogoini Primary School",
        ]:
            PollingStation.objects.get_or_create(name=name, ward=githiga)

        # ================= MARMANET =================
        for name in [
            "Naigera Primary School",
            "Ol' Ngarua Primary School",
            "Gatirima Primary School",
            "Thigio Primary School",
            "Karandi Primary School",
            "Kiambogo Primary School",
            "Karaba Primary School",
            "Kabage Primary School",
            "Chereta Primary School",
            "Lerematesho Primary School",
            "Kangumo Primary School",
            "Muhotetu Girls Secondary School",
            "Mairo Primary School",
            "Melwa Primary School",
            "Murichu Primary School",
            "Ndagara Primary School",
            "Oljabet Primary School",
            "Marmanet Social Hall",
            "King'uka Primary School",
            "Thiru Primary School",
            "Kwanjiku Primary School",
            "Mung'etho Primary School",
            "Manjani Primary School",
            "Gituamba Primary School",
            "Munyu Primary School",
            "Kirima Primary School",
            "Ng'arachi Primary School",
            "Lembus Primary School",
            "Gatami Primary School",
            "Kambi ya Simba Nursery School",
            "Muguongo Primary School",
            "Kiriti Primary School",
            "Siron Primary School",
        ]:
            PollingStation.objects.get_or_create(name=name, ward=marmanet)

        # ================= IGWAMITI =================
        for name in [
            "Muthengera Primary School",
            "St. Martin Muthengera Academy",
            "Kang'a Nderitu Community Plot",
            "Kundarilla Primary School",
            "Gatero Primary School",
            "Kite Primary School",
            "Rwathia Primary School",
            "P.C.E.A. Ngaindeithia Church & Pre-Primary School",
            "Waimungu Nursery School",
            "Kiandege Secondary School",
            "Nyahururu Municipal Council Social Hall",
            "Municipality Primary School",
            "Ngarenaro Primary School",
            "Starehe Primary School",
            "County Conference Centre",
            "Manguo Primary School",
            "Nyahururu Primary School",
            "Mariakani Primary School",
            "Maina Primary School",
            "Thama Primary School",
            "Nyahururu High School",
            "Nyandarua Boarding Primary School",
            "Shamanei Primary School",
            "Igwamiti Primary School",
            "Huho-ini Primary School",
            "Losogwa Primary School",
            "Uaso Narok Primary School",
            "Gitundaga Nursery School",
            "Mukurweini Police Post",
            "Silale Primary School",
            "Rugongo Primary School",
            "Karangi Primary School",
            "Kigumo Primary School",
            "Nakwakales Nursery School",
            "Siberia Nursery School",
            "Chemichemi Trading Centre",
            "Kirima Nursery School",
            "Mahianyu Primary School",
            "Mt. Angels Primary School",
            "Nyahururu Municipal Stadium",
            "Kaichakun Primary School",
            "Lokiriama Nursery School",
            "Bethel Primary School",
            "Munanda Primary School",
            "Kiheo Primary School",
            "St Bernard's Secondary School",
            "Kenya Wildlife Service Station Nyahururu",
            "Huruma Nursery School",
        ]:
            PollingStation.objects.get_or_create(name=name, ward=igwamiti)

        # ================= SALAMA =================
        for name in [
            "North Tetu Primary School",
            "Mathira Primary School",
            "Kiamariga Primary School",
            "Raya Primary School",
            "Mutara Primary School",
            "Marura Primary School",
            "Keriko Primary School",
            "Kisiriri Primary School",
            "Salama Primary School",
            "Ronda Primary School",
            "Muruku Primary School",
            "Nganoine Primary School",
            "Kiahiti Primary School",
            "Muruai Primary School",
            "Matigari Boarding Primary School",
            "Nguu Primary School",
            "Ngururiti Nursery School",
            "Kianjogu Primary School",
        ]:
            PollingStation.objects.get_or_create(name=name, ward=salama)

        self.stdout.write(self.style.SUCCESS("✅ Laikipia location data seeded successfully!"))