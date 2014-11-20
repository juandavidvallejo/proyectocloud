import boto.dynamodb
import boto.sqs
from django.conf import settings
from django.forms.models import model_to_dict
from boto.sqs.message import Message

def get_object(argument):
	if argument == "dynamo":
		dynamo_conn = boto.dynamodb.connect_to_region('us-west-1',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
		return dynamo_conn
	if argument == "sqs":
		sqs_conn = boto.sqs.connect_to_region('us-west-1',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
		return sqs_conn

def insert_nonrel(table, instance):
	metadata = model_to_dict(instance)
	model = dict((k, str(v)) for k, v in metadata.iteritems() if v)
	print model
	necessary = False
	conn = get_object("dynamo")
	try:
		insert_table = conn.get_table(table)
	except:
		table_schema = conn.create_schema(hash_key_name=str("new_hash_"+table),hash_key_proto_value=str, range_key_name=str("new_range_"+table),range_key_proto_value=str)
		insert_table = conn.create_table(name=table,schema=table_schema,read_units=1,write_units=1)
	item = insert_table.new_item(hash_key=str(model['id']), range_key=str(model['id']) , attrs=model)
	item.put()

def insert_async_message(queue_name, message):
	conn = get_object("sqs")
	try:
		my_queue = conn.create_queue(queue_name)
	except:
		my_queue = conn.get_queue(queue_name)
	m = Message()
	m.set_body(str(message))
	my_queue.write(m)

def process_queue(queue_name, value):
	conn_queue = get_object("sqs")
	conn_db = get_object("dynamo")
	my_queue = conn_queue.get_queue(queue_name)
	#get sqs messages
	rs = my_queue.get_messages()
	#process one at a time
	m = rs[0]
	id_db = m.get_body()
	#find db table and update range_key_proto_value
	table = conn_db.get_table("payment_plans")
	item = table.get_item(hash_key=id_db,range_key=id_db)
	item['risk_indicator'] = value
	item.put()
	my_queue.delete_message(m)