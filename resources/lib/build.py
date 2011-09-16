def string_to_list(elements):
	""" elements : string ("txt","md"...)"""
	elements_list = []
	for element in elements.split(','):
		element = element.replace('"', '')
		elements_list.append(element)
	return elements_list
