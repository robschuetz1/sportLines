import requests

game_ids = ['401114164','401111653','401110731','401114223','401117853','401117854','401117855','401119254','401119255','401114246','401114237','401119253','40111229','401114153','401117493','401112212','401117856','401114238','401112264','401112430','401112262','401114184','401112122','401110720','401110732','401112251','401110725','401112222','401112135','401114233','401112257','401112191','401112085','401112434','401114228','401112238','401112245','40111145','401112157','401112431','401112432','401112096','401110724','401110726','401110727','401112201','401112143','401119259','401117859','401117494','40111757','401119256','401110729','401110730','401121934','401110721','401112139','401112435','401117495','401114245','401121935','401114174','401114240','41114242','401114243','401119257','401119258','401117858','401112106','401110728','401112433','401114241','401114244','401112129','401128468','401117496','401117497','401114218','401112114','401112436','401121950','401121950']

game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='
r = requests.get(game_url + '401117854')
j = r.json()
jd = j.get("drives").get("previous")
penalty_plays = []

for game_id in game_ids:
	try:
		r = requests.get(game_url + game_id)
		j = r.json()
		jd = j.get("drives").get("previous")
		for drive in jd:
			plays = drive.get("plays")
			for play in plays:
				if play.get("text").lower().find('penalty') != -1 and play.get("type").get("text") != 'Penalty':
					penalty_plays.append([play.get("id"), play.get("type").get("text"), play.get("text")])
	except:
		print ('Bummer!  Game ID: ' + game_id + ' was not searched')


non_punt_penalties = []
					     
for p in penalty_plays:
    if p[1] not in ['Kickoff','Punt']:
            non_punt_penalties.append(p)

errors = []
search_strings = ['yds','yards','yd', 'yard', 'no gain','incomplete']

for x in non_punt_penalties:
    flag = 0
    position = []
    for s in search_strings:
        if x[2].find(s) != -1:
            try:
                pos = x[2].find(s)
                if s in ['no gain', 'incomplete']:
                    value = 0
                else:
                    value = int(x[2][pos - 3: pos - 1].strip(' '))
                flag = 1
                position.append([pos, value])
            except:
                pass
    if flag == 0:
        errors.append(x[2])
        is_error = 1
    else:
        is_error = 0

    first_pos = len(x[2])
    for p in position:
            if p[0] < first_pos:
                    first_pos = p[0]
                    final_value = p[1]
                    print (first_pos)

    if x[2][:first_pos].find('loss') != -1:
            final_value = -final_value
             
    print(x[0] + ', ' + str(final_value) + ', ' + str(is_error) + ':  ' + x[2])

print(len(errors))
