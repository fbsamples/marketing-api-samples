# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def seed_data(apps, schema_editor):
    # delete any existing sample data
    # then add the desired sample data
    Sample = apps.get_model("dash", "Sample")
    Sample.objects.all().delete()

    # >>> AUTO GENERATED SAMPLE OBJECTS
    # Regenerate with python manage.py gensamplemetadata

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="AccountListView",
        description="View a list of your ad accounts",
        view_module="samples.views.accountlist",
        seo_description="Facebook developers can view a list of your ad accounts using the Facebook Marketing API to accelerate Facebook marketing.",
        friendly_name="Account List",
        roles_to_check="",
        id="accounts")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="CustomAudienceView",
        description="Create custom audience",
        view_module="samples.views.customaudience",
        seo_description="Facebook developers can create Custom Audiences to accelerate Facebook marketing via the Facebook Custom Audiences API.",
        friendly_name="Custom Audiences",
        roles_to_check="",
        id="ca")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="AdCreationView",
        description="Create many ads using combinations of creative elements, links and targeting",
        view_module="samples.views.adcreation",
        seo_description="Developers can create many ads using combinations of creative elements, links and targeting to accelerate Facebook marketing via the Facebook API.",
        friendly_name="Creative Combinations",
        roles_to_check="",
        id="adcreation")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="AppEngagementView",
        description="Create mobile ads that deep link into your mobile app",
        view_module="samples.views.appengagement",
        seo_description="Facebook developers can create mobile ads that deep link into your mobile app via the Facebook App Engagement API to accelerate Facebook marketing.",
        friendly_name="App Engagement",
        roles_to_check="",
        id="appengagement")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="TieredLookalikeView",
        description="Create lookalike audiences with varying precision and size and bid accordingly",
        view_module="samples.views.tiered_lookalike",
        seo_description="Facebook developers can create lookalike audiences with varying precision and size and bid accordingly via the API to accelerate Facebook marketing.",
        friendly_name="Tiered Lookalike",
        roles_to_check="",
        id="tiered_lookalike")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="TargetingView",
        description="Intuitive UI for generating target spec that can be used in API calls",
        view_module="samples.views.targeting",
        seo_description="Facebook developers can test with the targeting specs setting and reach estimate via the API to accelerate Facebook marketing.",
        friendly_name="Targeting Spec",
        roles_to_check="",
        id="targeting")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="CarouselAdView",
        description="Create carousel link ads with up to 10 links",
        view_module="samples.views.carousel_ad",
        seo_description="Facebook developers can create Carousel Link ads with up to 10 links with the Carousel Link Ads API to accelerate Facebook marketing.",
        friendly_name="Carousel Link Ads",
        roles_to_check="",
        id="carousel")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="CarouselAppAdView",
        description="Create carousel ads for mobile app installs",
        view_module="samples.views.carousel_app_ad",
        seo_description="Facebook developers can create carousel ads for mobile app installs via the Carousel App Installs Ads API to accelerate Facebook marketing.",
        friendly_name="Carousel App Install Ads",
        roles_to_check="",
        id="carouselappad")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="AdsReportingView",
        description="Extract ad delivery and performance data",
        view_module="samples.views.ads_reporting",
        seo_description="Facebook developers can get ad reports via the Facebook Ads Reporting API to accelerate Facebook marketing.",
        friendly_name="Insights",
        roles_to_check="",
        id="adsreporting")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="ProductImageCheckView",
        description="Check product images for recommended size.",
        view_module="samples.views.product_image_check",
        seo_description="Facebook developers can automate checking of product catalog images for correct size.",
        friendly_name="Product Image Size Check",
        roles_to_check="",
        id="productimagecheck")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="ProductUpdateView",
        description="Update individual product in product catalog.",
        view_module="samples.views.product_update",
        seo_description="Facebook developers can update individual products by retailer ID via Facebook's Dynamic Product Ads (DPA) API to accelerate Facebook marketing.",
        friendly_name="DPA Product Update",
        roles_to_check="",
        id="productupdate")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="AppInstallAdView",
        description="Create mobile app install ads",
        view_module="samples.views.app_install_ad",
        seo_description="Facebook developers can create mobile app install ads via the Facebook App Install Ads API to accelerate Facebook marketing.",
        friendly_name="App Install Ad",
        roles_to_check="",
        id="app_install_ad")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="MultipleLalView",
        description="Create multiple lookalike audiences by country and percentage ratio",
        view_module="samples.views.multiple_lal",
        seo_description="Facebook developers can create lookalike audiences in multiple countries at multiple similarity ratios via the Facebook API.",
        friendly_name="Multiple Lookalike Audiences",
        roles_to_check="",
        id="multiple_lal")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="MacaCumulativeView",
        description="Mobile custom audiences based on cumulative events",
        view_module="samples.views.maca_cumulative",
        seo_description="Facebook developers can create custom audiences based on cumulative mobile app events to via the API to accelerate Facebook marketing.",
        friendly_name="Cumulative MACA",
        roles_to_check="",
        id="maca_cumulative")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="MacaFrequencyView",
        description="Mobile custom audiences based on app event frequency",
        view_module="samples.views.maca_frequency",
        seo_description="Facebook developers can create custom audiences based on the frequency of mobile app events using the Facebook Mobila App Custom Audience API.",
        friendly_name="Frequency MACA",
        roles_to_check="",
        id="maca_frequency")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="InstagramPotentialView",
        description="Find which ads have potential to run Instagram campaign",
        view_module="samples.views.instagram_potential",
        seo_description="Facebook developers can find which ads have potential to run Instagram campaigns via the Facebook Instagram Ad Analyzer API.",
        friendly_name="Instagram Ad Analyzer",
        roles_to_check="",
        id="instagram_potential")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="LeadAdView",
        description="Create lead ad",
        view_module="samples.views.lead_ad",
        seo_description="Facebook Developers can create lead ads to accelerate Facebook marketing via the Facebook Lead Ads API.",
        friendly_name="Create Lead Ad",
        roles_to_check="",
        id="lead_ad")

    Sample.objects.create(
        hide_in_gallery=True,
        view_class="OrderLevelReportingView",
        description="Retrieving order level reporting from the Facebook API.",
        view_module="samples.views.orderlevelreporting",
        seo_description="Facebook developers can retrieve order level reporting on ads using the Facebook Marketing API.",
        friendly_name="Order Level Reporting",
        roles_to_check="",
        id="orderlevelreporting")

    Sample.objects.create(
        hide_in_gallery=False,
        view_class="AudienceNetworkOptInView",
        description="Enable audience network on eligible adsets",
        view_module="samples.views.an_optin",
        seo_description="Audience Network opt in sample",
        friendly_name="Audience Network Optin",
        roles_to_check="",
        id="an_optin")

    Sample.objects.create(
        view_class="ProductAudienceEstimationView",
        description="Estimate your product audience",
        view_module="product_audience_estimation",
        seo_description="Facebook Product Audience Estimation",
        friendly_name="Product Audience Estimation",
        roles_to_check="",
        id="product_audience_est")

    Sample.objects.create(
        hide_in_gallery=True,
        view_class="AutobotConfigEditorView",
        description="Autobot config editor",
        view_module="autobot_config_editor",
        seo_description="Autobot config editor",
        friendly_name="Autobot config editor",
        roles_to_check="",
        id="autobot_config")

    # <<< AUTO GENERATED SAMPLE OBJECTS


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL('drop table if exists dash_sample;'),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False,
                 primary_key=True)),
                ('friendly_name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('view_module', models.CharField(max_length=50)),
                ('view_class', models.CharField(max_length=50)),
                ('hide_in_gallery', models.BooleanField(default=False)),
                ('roles_to_check', models.TextField(null=True)),
                ('seo_description', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='sample',
            options={'ordering': ['friendly_name']},
        ),
        migrations.RunPython(seed_data),
    ]
