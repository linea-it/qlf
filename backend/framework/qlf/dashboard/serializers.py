from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Job, Exposure, Camera, Process, Configuration, ProcessComment, Fibermap, Product
from clients import get_exposure_monitoring
from astropy.time import Time

qlf = get_exposure_monitoring()


# http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.

    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)


class JobSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            'pk', 'name', 'start', 'end', 'output',
            'status', 'version', 'logname', 'process',
            'camera', 'links'
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('job-detail', kwargs={'pk': obj.pk},
                            request=request),
        }


class ProcessSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Process
        fields = (
            'pk', 'pipeline_name', 'start', 'end',
            'status', 'version', 'process_dir', 'exposure',
            'links'
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('process-detail', kwargs={'pk': obj.pk},
                            request=request),
        }


class ProductSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'pk', 'value', 'key', 'mjd',
            'links'
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('product-detail', kwargs={'pk': obj.pk},
                            request=request),
        }


class ExposureSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Exposure
        fields = (
            'exposure_id', 'tile', 'telra', 'teldec',
            'dateobs', 'exptime', 'flavor', 'night',
            'airmass', 'program', 'links'
        )

    def get_links(self, obj):
        return {
            'self': reverse('exposure-detail', kwargs={'pk': obj.pk}),
         }


class FibermapSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Fibermap
        fields = (
            'fiber_ra', 'fiber_dec', 'fiber', 'objtype', 'links'
        )

    def get_links(self, obj):
        return {
            'self': reverse('fibermap-detail', kwargs={'pk': obj.pk}),
        }


class CameraSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = ('camera', 'spectrograph', 'arm', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('camera-detail', kwargs={'pk': obj.pk},
                            request=request),
         }


class ConfigurationSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Configuration
        fields = ('name', 'configuration', 'creation_date', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('configuration-detail', kwargs={'pk': obj.pk},
                            request=request),
         }


class ProcessJobsSerializer(serializers.ModelSerializer):

    process_jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = Process
        fields = ('id', 'exposure', 'process_jobs')


class ProcessingHistoryExposureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exposure
        fields = (
            'exposure_id', 'tile', 'telra', 'teldec',
            'dateobs', 'exptime', 'flavor', 'night',
            'airmass', 'program'
        )


class ProcessingHistorySerializer(DynamicFieldsModelSerializer):

    runtime = serializers.SerializerMethodField()
    datemjd = serializers.SerializerMethodField()
    exposure = ProcessingHistoryExposureSerializer(required=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Process
        fields = (
            'pk',
            'exposure',
            'datemjd',
            'runtime',
            'start',
            'end',
            'qa_tests',
            'comments_count',
            'status',
        )

    def get_runtime(self, obj):
        if obj.end is not None and obj.start is not None:
            return str(obj.end.replace(microsecond=0) - obj.start.replace(microsecond=0))
        else:
            return None

    def get_datemjd(self, obj):
        time = Time(str(obj.exposure.dateobs), format='iso', scale='utc')
        if time is None:
            return None
        else:
            return time.mjd

    def get_comments_count(self, obj):
        if not obj or not obj.process_comments:
            return None
        return obj.process_comments.count()


class ObservingHistorySerializer(DynamicFieldsModelSerializer):

    datemjd = serializers.SerializerMethodField()
    last_exposure_process_id = serializers.SerializerMethodField()
    last_exposure_process_qa_tests = serializers.SerializerMethodField()
    last_process_comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Exposure
        fields = (
            'exposure_id',
            'dateobs',
            'datemjd',
            'tile',
            'telra',
            'teldec',
            'exptime',
            'airmass',
            'last_exposure_process_id',
            'last_exposure_process_qa_tests',
            'flavor',
            'program',
            'last_process_comments_count',
            'night',
        )

    def get_datemjd(self, obj):
        time = Time(str(obj.dateobs), format='iso', scale='utc')
        if time is None:
            return None
        else:
            return time.mjd

    def get_last_exposure_process_id(self, obj):
        process = Process.objects.filter(exposure=obj.pk)
        if not process:
            return None
        return process.last().pk

    def get_last_exposure_process_qa_tests(self, obj):
        process = Process.objects.filter(exposure=obj.pk)
        if not process:
            return None
        return process.last().qa_tests

    def get_last_process_comments_count(self, obj):
        if not obj or not obj.process_exposure.last():
            return None
        return obj.process_exposure.last().process_comments.count()


class ExposuresDateRangeSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Exposure
        fields = ('exposure_id', 'dateobs')


class ExposureFlavorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Exposure
        fields = ('flavor',)


class ExposureNightSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Exposure
        fields = ('night',)


class ProcessCommentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = ProcessComment
        fields = ('id', 'text', 'user', 'date', 'process')
