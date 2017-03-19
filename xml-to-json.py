#!/usr/bin/env python3

import io
import json
import arrow
import xml.etree.ElementTree as ET

_input = './data/eponyms.xml'
_output = './export.json'
_main_elem = 'main'


def convert(source, target):
	js = read_and_convert(source)
	with io.open(target, 'w') as h:
		json.dump(js, h)

def read_and_convert(source):
	root = ET.parse(source).getroot()
	tags = []
	main = []
	
	# author
	andrew = {
		'_id': 'andrewyee',
		'type': 'author',
		'name': 'Andrew J Yee',
	}
	
	# find categories
	for category in root.iter('category'):
		tag = {
			'_id': category.get('tag').lower(),
			'type': 'tag',
			'content': {
				'en': category.get('title'),
			},
		}
		tags.append(tag)
	
	# find eponyms
	for eponym in root.iter('eponym'):
		epo = {
			'_id': eponym.get('id').lower(),
			'type': _main_elem,
			'tags': [cat.text.lower() for cat in eponym.iter('cat')],
			'content': {
				'en': {
					'name': eponym.find('name').text,
					'text': eponym.find('desc').text,
				}
			},
			'audits': [{
				'author': 'andrewyee',
				'date': arrow.get(eponym.find('c').text).format('YYYY-MM-DD'),
				'action': 'create',
			}],
		}
		main.append(epo)
			
	# concat
	docs = [andrew]
	docs.extend(tags)
	docs.extend(main)
	return {
		'date': arrow.get().isoformat(),
		'documents': docs,
	}


if '__main__' == __name__:
	convert(_input, _output)
