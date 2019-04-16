import json

import mongoengine as  mEngine

class schema():
    def __init__(self, db_name, coll_name, schema_json):
        super()
        self.__schema_cls = None
        self.db_name = db_name

        self.__db_name = db_name
        self.__coll_name = coll_name

        self.__schema_set = json.loads(schema_json)

    def get_schema_cls(self):
        if not self.__schema_cls:
            self.__schema_cls = type(self.__coll_name, (mEngine.Document, ), self.__mk_attribute_dict())
        
        return self.__schema_cls()

    # def swtch_collections(self, coll_name):
    #     self.__schema_cls.switch_collections()

    def set_schema_json(self, new_schema):
        self.__schema_set = json.loads(new_schema)

    def set_connection(self, db_name, host=None, port=None, username=None, password=None, auth_src=None):
        mEngine.connect(db=db_name, host=host, port=port, username=username, password=password, 
                        authentication_source=auth_src)

    def __mk_attribute_dict(self):
        attribute_dict = {}

        for key in self.__schema_set:
            if self.__schema_set[key]["type"] == "String":
                attribute_dict[key] = self.string_field(self.__schema_set[key])
            elif self.__schema_set[key]["type"] == "Integer":
                attribute_dict[key] = self.integer_field(self.__schema_set[key])
            elif self.__schema_set[key]["type"] == "Boolean":
                attribute_dict[key] = self.boolean_field(self.__schema_set[key])
            elif self.__schema_set[key]["type"] == "List":
                attribute_dict[key] = self.list_field(self.__schema_set[key])
            elif self.__schema_set[key]["type"] == "Dict":
                attribute_dict[key] = self.dict_field(self.__schema_set[key])
            elif self.__schema_set[key]["type"] == "EmbeddedDocument":
                attribute_dict[key] = self.embedded_document_field(self.__schema_set[key])
            elif self.__schema_set[key]["type"] == "Reference":
                attribute_dict[key] = self.reference_field(self.__schema_set[key])

        return attribute_dict
            
    def string_field(self, attrs_dict):
        return mEngine.StringField(regex=attrs_dict.get("regex"), max_length=attrs_dict.get("max_length"), min_length=attrs_dict.get("min_length"),
                    db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=attrs_dict.get("primary_key"),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))
            
    def integer_field(self, attrs_dict):
        return mEngine.IntField( max_value=attrs_dict.get("max_value"), min_value=attrs_dict.get("min_value"),
                    db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=attrs_dict.get("primary_key"),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))
            
    def list_field(self, attrs_dict):
        return mEngine.ListField( field=attrs_dict.get("field"),
                    db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=attrs_dict.get("primary_key"),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))
            
    def dict_field(self, attrs_dict):
        return mEngine.DictField( field=attrs_dict.get("field"),
                    db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=attrs_dict.get("primary_key"),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))
            
    def boolean_field(self, attrs_dict):
        return mEngine.BooleanField(db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                            unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=attrs_dict.get("primary_key"),
                            validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"),
                            sparse=attrs_dict.get("sparse"))
            
    def embedded_document_field(self, attrs_dict):
        return mEngine.EmbeddedDocumentField(document_type=attrs_dict.get("document_type"), db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), 
                                    default=attrs_dict.get("default"), unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), 
                                    primary_key=attrs_dict.get("primary_key"), validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), 
                                    null=attrs_dict.get("null"))
            
    def reference_field(self, attrs_dict):
        db_ref = False
        rd_rule = 0
        if attrs_dict.get("dbref"):
            db_ref = attrs_dict.get("dbref")
        if attrs_dict.get("reverse_delete_rule"):
            rd_rule = attrs_dict.get("reverse_delete_rule")
        return mEngine.ReferenceField(document_type=attrs_dict.get("document_type"), dbref=db_ref, reverse_delete_rule=rd_rule,
                            db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                            unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=attrs_dict.get("primary_key"),
                            validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

