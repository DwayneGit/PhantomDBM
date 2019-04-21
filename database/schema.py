import json

import mongoengine as  mEngine

class schema():
    def __init__(self, db_name, coll_name, schema_json, ref_schemas):
        super()
        self.__schema_json = schema_json
        self.__ref_schemas = ref_schemas
        
        self.__schema_cls = None
        self.__ref_schema_cls_dict = {}

        self.db_name = db_name

        self.__db_name = db_name
        self.__coll_name = coll_name
    
    def build_document(self, doc, schema_cls=None, level=0):
        empty_doc_flag = True
        new_doc = schema_cls
        tmp = {}
        if not schema_cls:
            new_doc = self.get_schema_cls()
        if level == 0:
            tmp = json.loads(self.__schema_json)
        # print("Hello " + str(level))
        for field in doc:
            if hasattr(new_doc, field):
                # print(tmp.get(field))
                if level == 0 and (tmp[field].get("type") == "EmbeddedDocument" or tmp[field].get("type") == "Reference"):
                    setattr(new_doc, field, self.build_document(doc[field], self.__ref_schema_cls_dict[tmp[field]["document_type"]](), level+1))
                else:
                    setattr(new_doc, field, doc[field])
                empty_doc_flag = False
        
        if empty_doc_flag:
            return None

        return new_doc
            # print(attr_dict[field])
        # print(type(new_doc))

    def get_schema_cls(self, schema="Main"):
        if schema == "Main" and not self.__schema_cls:
            self.__schema_cls = self.__mk_schema_cls(self.__coll_name, mEngine.Document, self.__schema_json)
        return self.__schema_cls()

    def get_ref_schema_cls_dict(self):
        return self.__ref_schema_cls_dict

    def __mk_schema_cls(self, collection, super_cls, schema_json):
        try:
            return type(collection, (super_cls, ), self.__mk_attribute_dict(json.loads(schema_json)))
        except json.decoder.JSONDecodeError as err:
            print(err)
            return False
    # def swtch_collections(self, coll_name):
    #     self.__schema_cls.switch_collections()

    def set_schema_json(self, new_schema):
        self.__schema_json = new_schema
        self.__schema_cls = self.__mk_schema_cls(self.__coll_name, mEngine.Document, self.__schema_json)
    
    def get_schema_json(self):
        return self.__schema_json

    def set_connection(self, db_name, host=None, port=None, username=None, password=None, auth_src=None):
        mEngine.connect(db=db_name, host=host, port=port, username=username, password=password,
                        authentication_source=auth_src)

    def __mk_attribute_dict(self, attr_set):
        attribute_dict = {}

        for key in attr_set:
            if attr_set[key]["type"] == "String":
                attribute_dict[key] = self.string_field(attr_set[key])
            elif attr_set[key]["type"] == "Integer":
                attribute_dict[key] = self.integer_field(attr_set[key])
            elif attr_set[key]["type"] == "Boolean":
                attribute_dict[key] = self.boolean_field(attr_set[key])
            elif attr_set[key]["type"] == "List":
                attribute_dict[key] = self.list_field(attr_set[key])
            elif attr_set[key]["type"] == "Dict":
                attribute_dict[key] = self.dict_field(attr_set[key])
            elif attr_set[key]["type"] == "EmbeddedDocument":
                attribute_dict[key] = self.embedded_document_field(attr_set[key])
            elif attr_set[key]["type"] == "Reference":
                attribute_dict[key] = self.reference_field(attr_set[key])

        # print(attribute_dict)
        return attribute_dict

    def string_field(self, attrs_dict):
        return mEngine.StringField(regex=attrs_dict.get("regex"), max_length=attrs_dict.get("max_length"), min_length=attrs_dict.get("min_length"),
                    db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

    def integer_field(self, attrs_dict):
        return mEngine.IntField(max_value=attrs_dict.get("max_value"), min_value=attrs_dict.get("min_value"),
                    db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

    def list_field(self, attrs_dict):
        return mEngine.ListField(field=attrs_dict.get("field"),
                    db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

    def dict_field(self, attrs_dict):
        return mEngine.DictField(field=attrs_dict.get("field"),
                    db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

    def boolean_field(self, attrs_dict):
        return mEngine.BooleanField(db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                            unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                            validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"),
                            sparse=attrs_dict.get("sparse"))

    def embedded_document_field(self, attrs_dict):
        if not self.__ref_schemas.get(attrs_dict["document_type"]):
            return "no schema for given document type"
        # print(self.__ref_schemas.get(attrs_dict["document_type"]))
        if not self.__ref_schema_cls_dict.get(attrs_dict["document_type"]):
            self.__ref_schema_cls_dict[attrs_dict["document_type"]] = self.__mk_schema_cls(attrs_dict["document_type"], mEngine.EmbeddedDocument, self.__ref_schemas.get(attrs_dict["document_type"]))
        
        # print(ref_cls)
        return mEngine.EmbeddedDocumentField(document_type= self.__ref_schema_cls_dict[attrs_dict["document_type"]], db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"),
                                    default=attrs_dict.get("default"), unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"),
                                    primary_key=string_to_bool(attrs_dict.get("primary_key")), validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"),
                                    null=attrs_dict.get("null"))

    def reference_field(self, attrs_dict):
        if not self.__ref_schemas.get(attrs_dict["document_type"]):
            return "no schema for given document type"

        db_ref = False
        rd_rule = 0

        if attrs_dict.get("dbref"):
            db_ref = attrs_dict["dbref"]
        if attrs_dict.get("reverse_delete_rule"):
            rd_rule = attrs_dict["reverse_delete_rule"]

        if not self.__ref_schema_cls_dict.get(attrs_dict["document_type"]):
            self.__ref_schema_cls_dict[attrs_dict["document_type"]] = self.__mk_schema_cls(attrs_dict["document_type"], mEngine.Document, self.__ref_schemas.get(attrs_dict["document_type"]))
        
        return mEngine.ReferenceField(document_type= self.__ref_schema_cls_dict[attrs_dict["document_type"]], dbref=db_ref, reverse_delete_rule=rd_rule,
                            db_field=attrs_dict.get("db_field"), required=attrs_dict.get("required"), default=attrs_dict.get("default"),
                            unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                            validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

    def get_field(self, field_str, doc_type=None):
        if (field_str == "EmbeddedDocument" or field_str == "Reference") and not doc_type:
            print("No document type given for given field")
        elif field_str == "EmbeddedDocument":
            return self.embedded_document_field(self.__ref_schemas[doc_type])
        elif field_str == "Reference":
            return self.reference_field(self.__ref_schemas[doc_type])

def string_to_bool(string):
    if string is None:
        return None
    elif string == "False":
        return False
    elif string == "True":
        return True
    else:
        raise IOError