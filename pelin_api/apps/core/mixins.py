class DynamicFieldsSerializer(object):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        remove_fields = kwargs.pop('remove_fields', None)
        super(DynamicFieldsSerializer, self).__init__(*args, **kwargs)

        if fields:
            [self.fields.pop(field) for field in self.fields if
             field not in fields]

        if remove_fields:
            [self.fields.pop(field) for field in self.fields if
             field in remove_fields]


class RequestContextSerializer(object):
    def __init__(self, *args, **kwargs):
        super(RequestContextSerializer, self).__init__(*args, **kwargs)

        if self.context.get('request'):
            self.request = self.context.get('request')
            self.user = self.context.get('request').user
