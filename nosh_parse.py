#! /usr/bin/python

import sys
import urllib2
import csv
import html_utils
from BeautifulSoup import BeautifulSoup

def fetch_page(url):
    """
    Fetches the content from given url
    @param name of the url
    @return html data present at the url
    """
    try:
        response = urllib2.urlopen(url)
        return response.read()

    except urllib2.HTTPError, e:
        print "Error code: %s" % e.code
        return
        
    except urllib2.URLError, e:
        print "Error!", e.args
        return

def get_menu(raw_data):
    """
    parses HTML data and gets the menu list
    @params HTML data
    @return menu list of the restaurant
    """
    menu_list = []
    
    tree = BeautifulSoup(raw_data)
    menu_tree = tree.find('div',{'id':'menu-item-list'})
    tables = menu_tree.findAll('table')
    for single_table in tables:
        ## finding the item
        item_name = single_table.find('div',{'class':'ow-check-in-mi'}).text
        ## finding description; it may or may not be present
        item_description = single_table.find('div',\
        																		{'class':'ow-check-in-review'})
        if item_description == None:
            item_description = ""
        else:
            item_description = item_description.text
        ## adding to the menu_list after striping HTML enttites from text
        menu_list.append((html_utils.strip_html(item_name),\
        									html_utils.strip_html(item_description)))
        
    return menu_list
        
def write_to_csv(menu_list,file_id):
    """
    writes the menu list to a csv file
    @params - menu list and restaurant id
    @return - A csv file gets created
    """
    filename = file_id+'.csv'
    file_handler = open(filename,'w')
    csv_handler = csv.writer(file_handler, delimiter = '\t')
    
    for row in menu_list:
        item_name,item_description = row
        csv_handler.writerow([item_name.encode('utf8'),\
        										item_description.encode('utf8')])
    file_handler.close()
    return
        
def main():
    """
    drives the entire processing
    @params - Nothing. Parameters are read from command line
    @result - A CSV file gets creating having the menu items 
    and their descriptions
    """
    if len(sys.argv) < 2:
        print "Usage:",sys.argv[0],"url_name"
        return;
    url_name = sys.argv[1]
    raw_data = fetch_page(url_name)
    if raw_data is not None:
        menu_list = get_menu(raw_data)
        file_id = url_name.split('/')[-1]
        write_to_csv(menu_list,file_id)


if __name__ == '__main__':
    main()