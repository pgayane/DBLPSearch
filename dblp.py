import requests
import argparse

def get_papers(query, top):
  payload = {'q':query, 'format':'json'}
  if top != 0:
	payload['h'] = top

  r = requests.get("http://www.dblp.org/search/api/", params=payload)
  result = r.json()

  if int(result['result']['hits']['@sent']) == 0:
    return []

  hits = result['result']['hits']['hit']
  if isinstance(hits, dict):
    hits = [hits]

  return [{'title': hit['info']['title']['text'],
             'author':hit['info']['authors']['author'],
             'year':hit['info']['year'],
             'doi':hit['info']['title']['@ee'],
             'url':hit['url']} for hit in hits]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Searches DBLP')
	parser.add_argument('query', nargs = "?", help='Search query')
	parser.add_argument('--title', help='Print title')
	parser.add_argument('--author', help='Print author')
	parser.add_argument('--top', type=int, default = 0, help='Only print top n match')

	args = parser.parse_args()

	query = ''
	if args.query:
		query = args.query
		
	if args.author:
		if query:
			query += '+'
		query += 'ce:author:'+args.author.lower().replace(' ', '_')
	
	if args.title:
		if query:
			query += '+'
		query += args.title
		
	results = get_papers(query, args.top)
  
	for paper in results:
		print 'Title:', paper['title']
		print 'Author:', ', '.join(paper['author'])
		print 'Year:', paper['year']
		print 'DOI:', paper['doi']
		print 'URL:', paper['url']
		print '\n'

	
	