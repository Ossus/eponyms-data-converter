#!/usr/bin/env python3

import io
import json
import arrow
import xml.etree.ElementTree as ET

_input = './data/eponyms.xml'
_output = './export.json'
_main_elem = 'element'


def convert(source, target):
	js = read_and_convert(source)
	with io.open(target, 'w') as h:
		json.dump(js, h)

def read_and_convert(source):
	root = ET.parse(source).getroot()
	categories = []
	eponyms = []
	audits = []
	
	# author
	andrew = {
		'_id': 'andrewyee',
		'type': 'author',
		'name': 'Andrew J Yee',
	}
	
	# find categories
	for category in root.iter('category'):
		cat = category.attrib
		cat['_id'] = cat.get('tag').lower()
		cat['type'] = 'category'
		del cat['tag']
		categories.append(cat)
	
	# find eponyms
	for eponym in root.iter('eponym'):
		epo = {
			'_id': eponym.get('id').lower(),
			'type': _main_elem,
			'name': eponym.find('name').text,
			'text': eponym.find('desc').text,
			'categories': [cat.text.lower() for cat in eponym.iter('cat')],
		}
		audit = {
			'_id': 'aud_{}'.format(epo['_id']),
			'type': 'audit',
			'agent': 'andrewyee',
			'date': arrow.get(eponym.find('c').text).format('YYYY-MM-DD'),
			'action': 'create',
			'target': epo['_id'],
		}
		eponyms.append(epo)
		audits.append(audit)
			
	# concat
	return {
		'authors': [andrew],
		'categories': categories,
		'elements': eponyms,
		'audits': audits,
	}


if '__main__' == __name__:
	convert(_input, _output)
