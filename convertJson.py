import json
import csv
import time
import os
from config import Config
 
def get_formatted_lines(file_name):
    """
    :param file_name: File name for file that requires formatting.
    :return lines: List of Formatted lines 
    """
    lines = []
    lines.append('[')
    with open(file_name, 'r') as f:
        content = f.readlines()
        for line in content:
            lines.append('%s,'  % (line))
    lines.append(']')
    return lines

def write_to_new_file(file_name, lines):
    """
    :param file_name: Name of file to write newly formatted lines.
    :param lines: Lines you want to write out to the file
    :return:
    """
    with open(file_name , 'w') as file:
        for line in lines:
            file.write(line)

def main():

    for file_name in [f for f in os.listdir(Config.data) if (f.endswith('.csv')) and (f.find('preprocessed') < 1)]:

        out_filename = file_name.split('.')[0] + '_preprocessed.csv'
        csv_out = open(Config.prep_data + out_filename, mode='w')  # opens csv file to write to
        writer = csv.writer(csv_out, delimiter='\t')  # create the csv writer object

        fields = ['date', 'text', 'screen_name', 'followers', 'friends', 'country', 'place_name', 'lat', 'lon', 'rt',
                  'fav', 'url','tags']  # field names
        writer.writerow(fields)  # writes field

        #file_name=
        with open(Config.data + file_name, 'r') as f:
            reader = csv.reader(f)
            city = Config.city
            num_tw=0
            num_geo_tw=0
            num_geo_dub_tw=0
            w_num_geo_dub_tw=0
            num_ll_dub_tw=0
            coord_without_name=0
            for row in reader:
                #writes a row and gets the fields from the json object
                #screen_name and followers/friends are found on the second level hence two get methods
                line = json.loads(row[0])#row is a list with one string which is the json object required by json.loads
                num_tw=num_tw+1
                lat='NA'
                long='NA'
                ll=0
                if (line.get('geo')!=None):
                    if ('coordinates' in  line.get('geo')) and (line["geo"]["coordinates"] != None):
                        long=line["geo"]["coordinates"][0]
                        lat=line["geo"]["coordinates"][1]
                        num_geo_tw=num_geo_tw+1
                        ll=1
                    #else:
                        #uncomment if you want all data points, even with NA lat long
                        #continue
                #else:
                    #uncomment if you want all data points, even with NA lat long
                    #continue
                country = 'NA'
                place_full_name='NA'
                if(line.get('place') !=None):
                    if 'country' in line.get('place'):
                        country=line.get('place').get('country')
                    if('full_name' in line.get('place')):
                        place_full_name=line.get('place').get('full_name')
                dateproc = line.get('created_at')
                try:
                    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(dateproc,'%a %b %d %H:%M:%S +0000 %Y'))
                except:
                    continue
                urls=line.get("entities").get("urls")
                if len(urls) > 0:
                   urls=urls[0]
                   url=urls.get('expanded_url')
                else:
                   url="NA"
                ff= line.get('favorite_count')
                tags=line.get("entities").get("hashtags")

          #      ff=str(ff).replace(u'\xed','0')
     #    #       ff=int(ff)
    #            print(ff)
                if  (place_full_name=="NA") & (ll==1) : coord_without_name=coord_without_name+1
                if  (place_full_name.lower().find(city) >=0) :
                    num_geo_dub_tw=num_geo_dub_tw+1
                    if ll==1: num_ll_dub_tw= num_ll_dub_tw +1
                    try:
                        w_num_geo_dub_tw=w_num_geo_dub_tw+1
                        writer.writerow([ts,
                                line.get('text').encode('unicode_escape'), #unicode escape to fix emoji issue
                                line.get('user').get('screen_name'),
                                line.get('user').get('followers_count'),
                                line.get('user').get('friends_count'),
                                country,
                                place_full_name,
                                lat,
                                long,
                                line.get('retweet_count'),
                                ff, url,tags ])
                    except:
                        pass
        csv_out.close()
        print(file_name.split('.')[0] + " total: "+str(num_tw) +" total geo: "+str(num_geo_tw)+ city + "  tws: " + str(num_geo_dub_tw)+"lat-lon "+city+" tweets: "+ str(num_ll_dub_tw)+"tws without a label but with coords "+str(coord_without_name)+" written tws " +str(w_num_geo_dub_tw) )

if __name__ == "__main__":
    main()

    #Test file:
    #input_file=    open(out_filename, 'r')
    #csv_reader = csv.reader(input_file, delimiter=.separator)
    #header = next(csv_reader)
    #text_column_index = header.index('text')
