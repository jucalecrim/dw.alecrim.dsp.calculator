
import names
from random_address import real_random_address
import random
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import ceil
import numpy as np

def name_generator(size, gender = 'random'):
    if size == 0:
        size = random.choice(range(5,80))
        
    name_list = []
    if gender == 'random':
        for i in range(size):
            name_list.append(names.get_full_name())
    else:
        for i in range(size):
            name_list.append(names.get_full_name(gender=gender))
    return name_list

def name_dataset(name_list):
    dicty = {"dw_id":[], "name":[], "id_type":[], "id_number":[], "gender":[], "age":[], "height":[], "weight":[], "address":[], "city":[], "state":[], "zip":[]}
    # df = pd.DataFrame(dicty)
    for i in name_list:
        dicty["dw_id"].append((i[:2].upper()+"_001"))
        dicty["name"].append(i)
        doct = random.choice(["RG", "CPF"])
        dicty["id_type"].append(doct)
        if doct:
            doct_info = str(random.choice(range(9))) + str(random.choice(range(9))) + "." + str(random.choice(range(9))) + str(random.choice(range(9))) + str(random.choice(range(9))) + "." + str(random.choice(range(9))) + str(random.choice(range(9))) + str(random.choice(range(9))) + "-" + str(random.choice(range(9))) + str(random.choice(range(9))) 
        else:
            doct_info = str(random.choice(range(9))) + str(random.choice(range(9))) + str(random.choice(range(9))) + "." + str(random.choice(range(9))) + str(random.choice(range(9))) + str(random.choice(range(9))) + "." + str(random.choice(range(9))) + str(random.choice(range(9))) + str(random.choice(range(9))) + "/" + str(random.choice(range(9))) + str(random.choice(range(9))) 
        dicty["id_number"].append(doct_info)
        del doct, doct_info
        dicty["gender"].append(random.choice(["male", "female"]))
        dicty["age"].append(random.randrange(5,100))
        dicty["height"].append(random.randrange(100,200 , 3)/100)
        dicty["weight"].append(random.randrange(40,120, 3))
        address = real_random_address()
        dicty["address"].append(address.get("address1"))
        dicty["city"].append(address.get("city"))
        dicty["state"].append(address.get("state"))
        dicty["zip"].append(address.get("postalCode"))
        del address
        # df = pd.concat([df, pd.DataFrame(dicty)], axis = 0)
    return dicty

def quota_calculator(o, n, t, dim, qi, qt, pt, method = 'alfa'):
    """
            o	quantidade de ofertas que a dWallet participou
            n	total de contribuições por plano
            t	Tempo em meses que o participante está participando no plano
            dim	Soma Total (ou DIM médio) de DIM que cada usuário possui nos NS que contribuem pro plano
            qi	Quotas Iniciais
            qt	Total de Cotas Iniciais
            pt	Peso de tempo
            
            Alfa = (((qi * t)*pt + n*dim*(1-pt))*(1+o))/qt = Standard Base Line Formula
            Beta = (((t)*pt + n*dim*(1-pt))*(1+o))/qt = No Qi and Qt is equal to number of members
            Gamma = (((qi * t)*pt + n*(1-pt))*(1+o))/qt = Standard but no DIM
            Delta = (((qi * t)*pt + dim*(1-pt))*(1+o))/qt = Standard but no N
            
"""
    if method == 'beta':
        return (((t)*pt + n*dim*(1-pt))*(1+o))/qt
    elif method == 'gamma':
        return (((qi * t)*pt + n*(1-pt))*(1+o))/qt 
    elif method == 'delta':
        return (((qi * t)*pt + n*(1-pt))*(1+o))/qt 
    else:
        return (((qi * t)*pt + n*dim*(1-pt))*(1+o))/qt

def fill_db(members, plan_info, start_date, start_date_random, random_N, random_DIM):
    dsp = list(plan_info.keys())[0]
    ns = plan_info.get(dsp).get('ns')
    # members = list(name_df['dw_id'])
    n_pop = range(len(members))
    if type(start_date) == str:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    df_full = {}
    dicty = {}
    for j in ns:
        if random_N:
            N = [random.choice(range(0,100)) for i in n_pop]
        else:
            N = [5 for i in n_pop ] #if not random default is 5
            
        if random_DIM:
            DIM = [random.choice(range(0,10)) for i in n_pop] 
        else:
            DIM = [2 for i in n_pop] # if not random default is 2
            
        if start_date_random:
            start_list = [start_date + relativedelta(months=random.choice(range(0,12))) for i in n_pop]
        else:
            start_list = [start_date for i in n_pop]
            
        dicty = pd.DataFrame({'name':members, 'start_date':start_list, 'ns':[j for i in n_pop],'N':N, 'DIM':DIM})
        df_full = pd.concat((pd.DataFrame(df_full), dicty), axis = 0)
    df_full.index = range(df_full.shape[0])
    df_full = df_full.drop(df_full[(df_full.N == 0) | (df_full.DIM == 0)].index)
    
    return df_full

def sp_stocks():
    try:
        
        import requests
        from bs4 import BeautifulSoup
    
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
        # Send a GET request to the URL
        response = requests.get(url)
    
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
    
            # Find the table containing the S&P 500 tickers
            table = soup.find('table', {'class': 'wikitable'})
    
            # Extract data from the table
            data = []
            for row in table.find_all('tr')[1:]:
                columns = row.find_all(['td', 'th'])
                ticker = columns[0].text.strip()
                industry = columns[2].text.strip()
                name = columns[1].text.strip()
                data.append([ticker, name, industry])
    except:
        print("ERROR CONNECTING TO WIKI")
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")
        data = {"Ticker":["MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL", "A", "ADP", "ABNB", "AKAM", "ALB", "ARE"], 
                "Company Name":["3M", "A O Smith", "Abbott","AbbVie", "Accenture", "Adobe Inc", "Advanced Micro Devices", "AES Corporation", "AFLAC", "Aligent Tecchnologies","Air Products and Chemicals", "Airbnb", "Akamai", "Albermarle Corporation", "Alexandra Real Estates Equities"], 
                "Industry":["Industrials", "Industrials", "Health Care", "Health Care", "Information Technology", "Information Technology", "Information Technology", "Utilities", "Financials", "Health Care", "Materials", "Consumer Discretionary", "Information Technology", "Materials", "Real Estate"]}

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=['Ticker', 'Company Name', 'Industry'])
    return df
        
        
def plans(action, plan_info, plan_ds = {}):
    """ action = 1 - edit
        action = 2 - add
        action = 3 - remove 
        
        plan dict format if action != 1

        {"plan_name":{"id":"plan id",
                    "category":"plan category", 
                    "start_date":"string in ymd format of creation date"
                    "ns":[list of named schemas associated with the plan]}}
        
        """
    if action == 3:
        del plan_ds[plan_info]
        print("Plan '{}' removed sucessfully".format(plan_info))
    else:
        pi = list(plan_info.keys())[0]
        if action == 2:
            plan_ds[pi] = plan_info[pi]
            print("Plan '{}' added sucessfully".format(pi))
        else:
            plan_ds.update({pi:plan_info[pi]})
            print("Plan '{}' updated sucessfully".format(pi))
        
    return plan_ds

def random_offer_generator(company_info, ns_list, dsp_target, price, offer_creation_date):
    use_cases = ['Market Research',
                'Customer Insights',
                'Lead Generation',
                'Risk Management',
                'Healthcare Analytics',
                'Financial Analysis',
                'Supply Chain Optimization',
                'Human Resources',
                'Government and Public Policy',
                'Energy and Utilities',
                'Advertising and Marketing',
                'Educational Analytics']

    offer = {company_info.get("ticker") + "_001":{"creator_id": company_info.get("ticker")+ "__DW",
                  "offer_name":company_info.get("industry") + " " + random.choice(use_cases) + " Offer",
                  "creation_date":offer_creation_date,
                  "product":{"offer_category":"buy",
                            "offer_type": "dsp",
                            "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin eu ligula ultricies massa rutrum rhoncus. Phasellus consequat finibus interdum. Duis consequat enim vel nulla efficitur, nec finibus odio vehicula. Proin euismod, lectus non accumsan auctor, enim nisi molestie nisl, ut sagittis lectus urna id nibh. Vestibulum malesuada libero molestie, scelerisque magna a, convallis massa. Integer quis tortor vel quam blandit pellentesque a vel neque. Pellentesque auctor ex eu tortor aliquam, sit amet pharetra nibh mattis. Curabitur vitae scelerisque nulla. Cras ut eros id enim sodales sodales vitae quis odio.",
                            "end_use":random.choice(["licensing", "dApp", "API"]),
                            "period":{"unit":random.choice(["D", "M", "Y"]), "value":random.choice(range(50))},
                            "frequency":{"unit":random.choice(["RT", "H", "D", "M", "Y"]), "value":random.choice(range(50))},
                            "target":{"targeted":dsp_target},                                
                            "ns_attributes":ns_list,
                            "terms_conditions":"XXXXXXX"},
                 
                  "price":{"monetization_engine":"cash_now",
                          "payment_terms":"upfront",
                          'price':{'unit':'BRL', 'value':price},
                          "share_custody_tc":"50% to patient 50% to lab",
                          "delivery":"virtual"},
                 
                  "place":{"region":"br"},
                 
                  "promotion":{
                      "offer_duration":{"unit":random.choice(["H", "D", "M"]), "value":random.choice(range(10))},
                      "offer_promotion":"False",
                      "front_end":""}
                  }
      }
    return offer

def offer_loop(plan_info, length, rand_price, price):
    if length == 0:
        length = random.choice(range(3,9))
    plan_name = list(plan_info.keys())[0]
    ns_list = plan_info.get(plan_name).get('ns')
    min_creation_date = plan_info.get(plan_name).get('start_date')
    
    #price = [random.choice(range(1000,10000)) if rand_price else 1000][0]
    #min_creation_date + relativedelta(months = random.choice(range(0,12)))
    sp_stocks_df = sp_stocks()
    dicty = {}
    index_list = [random.choice(range(sp_stocks_df.shape[0])) for i in range(length)]
    
    for i in index_list:    
        company_info = {'ticker':sp_stocks_df['Ticker'][i], 'company':sp_stocks_df['Company Name'][i], 'industry':sp_stocks_df['Industry'][i]}
        if rand_price:
            price = random.choice(range(price,price*5))
        
        offer_creation_date = datetime.strptime(min_creation_date,'%Y-%m-%d') + relativedelta(months = random.choice(range(0,12)))
        rog = random_offer_generator(company_info, ns_list = ns_list, dsp_target = plan_name, price = price, offer_creation_date = offer_creation_date)
        dicty[list(rog.keys())[0]] = rog
    return dicty

def plot_graph(qa_df, path, n_bars = 10):
    import plotly.express as px
    import plotly.io as bpm

    height = list(qa_df['cash'])
    limit = max(height)/n_bars
    limit = int(round(limit, 0) if limit < 100 else round(limit, -1)) #possible error
    limit_list = list()
    for i in range(1, n_bars):
        limit_list.append(limit*i)
    bar = []
    for i in range(0,len(limit_list)):
        # bar.append(sum((height > limit_list[i-1]) & (height <= limit_list[i])))
        test =  sum([(j >  limit_list[i-1]) & (j <= limit_list[i]) for j in height])
        bar.append(test)
    # y_pos = np.arange(len(bar)
    bpm.orca.config.save()
    fig = px.bar(pd.DataFrame({"Cash":np.array(limit_list), "Count":np.array(bar)}), x="Cash", y="Count")
    fig.update_traces(marker_color='green')
    fig.update_layout(
        font_family="Courier New",
        font_color="blue",
        title_font_family="Times New Roman",
        title_font_color="blue",
        title_font_size =36,
        legend_title_font_color="green",
        title_text="Monetization Distribution", title_x=0.5
    )
    fig.show()
    if path != "C:\\user\\img.png":
        fig.write_image(path, engine= 'orca')

def find_member_offer(offer_db, members_ns_db):
    dicty = {}
    for j in members_ns_db['name'].unique():
        df_cut = members_ns_db[members_ns_db['name'] == j]
        ns_list = list(df_cut['ns'].unique())
        entry_date = list(df_cut['start_date'].unique())[0]
        entry_date = datetime.strptime(entry_date, "%Y-%m-%d") if type(entry_date) == str else entry_date
        
        o_count = []
        for i in offer_db.keys():
            creation_date = offer_db[i][i].get('creation_date')
            creation_date = datetime.strptime(creation_date, "%Y-%m-%d") if type(creation_date) == str else creation_date
            offer_ns_list = offer_db[i][i].get('product').get('ns_attributes')
            o_count.append(True if True in [True if (p in ns_list) & (creation_date >= entry_date) else False for p in offer_ns_list] else False)
        
        o_pf = sum(o_count)
        dicty[j] = o_pf
    
    return pd.DataFrame({"name":[i for i in dicty.keys()], "o":[dicty.get(i) for i in dicty.keys()]})

def dist_calculation(plan_info, offers, member_ns_df, qi, pt, method):
    # o = len(offers.keys())
    m = 0
    qt = len(member_ns_df['name'].unique()) * qi
    
    for i in list(offers.keys()):
        m = m + offers[i].get(i).get('price').get('price').get('value')
        
    o_df = find_member_offer(offer_db = offers, members_ns_db = member_ns_df)
    member_ns_df = member_ns_df.merge(o_df, on = "name", how = "left")
    
    member_ns_df['t'] = [ceil((i - datetime.strptime(plan_info.get(list(plan_info.keys())[0]).get('start_date'), '%Y-%m-%d') ).days / 30) for i in member_ns_df['start_date']]
    
    qa_dicty = {}
    for i in member_ns_df['name'].unique():
        df_cut = member_ns_df[member_ns_df['name'] == i]
        qa = quota_calculator(max(df_cut['o']), sum(df_cut['N']), max(df_cut['t']) , np.mean(df_cut['DIM']), qi, qt, pt, method)
        q_temp = {'name':i, 'qa':qa}
        qa_dicty[i] = q_temp
        
    tot = sum([qa_dicty.get(i).get('qa') for i in qa_dicty.keys()])
    
    for i in qa_dicty.keys():
        qa_dicty.get(i)['cash'] = m*(qa_dicty.get(i).get('qa')/tot)
    qa_df = pd.DataFrame(qa_dicty).transpose()
    qa_df.index = range(qa_df.shape[0])
    
    member_ns_df = member_ns_df.merge(qa_df, on = "name")
    del qa_dicty, i, qa, df_cut, o_df, q_temp, offers, plan_info
    
    if method == 'beta':
        formula = "(((T)*Pt + N*DIM*(1-Pt))*(1+O))/Qt = no Qi and Qt is equal to number of members"
    elif method == 'gamma':
        formula = "(((Qt * T)*Pt + N*(1-Pt))*(1+O))/Qt = Standard Formula with no DIM"
    elif method == 'delTa':
        formula = "(((Qt * T)*Pt + DIM*(1-Pt))*(1+O))/Qt = Standard buT no N"
    else:
        formula = "(((Qt * T)*Pt + N*DIM*(1-Pt))*(1+O))/Qt = Standard Base LiNe Formula"

    dicty = {"qa_df":qa_df, "m":m, "qi":qi, "qt":qt, "pt":pt,"formula":formula,"pay_formula":method, "members_df":member_ns_df}
    return dicty

def offer_html(offer_name, offer_category, creator_id, description, end_use, period, frequency, target, ns_attributes, terms_conditions, monetization_engine, payment_terms, price , share_custody_tc, delivery, region, offer_duration, offer_promotion):
    div_a = """<div style='margin-top:5.0pt;margin-right:0cm;margin-bottom:10.0pt;margin-left:0cm;line-height:115%;font-size:15px;font-family:"Aptos",sans-serif;border:solid #C1E4F5 3.0pt;padding:0cm 0cm 0cm 0cm;background:#C1E4F5;'>
    <h2 style='margin-top:5.0pt;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:115%;background:#C1E4F5;border:none;padding:0cm;font-size:13px;font-family:"Aptos",sans-serif;font-weight:normal;'><span style="color: black; font-size: 15px;"><strong>{offer_name}</strong></span></h2>
</div>""".format(offer_name = offer_name)

    html =     """
    {div_a}
    
    <p><strong>Offer Type</strong>: {offer_category}</p>
    <p><strong>Created By</strong>: {creator_id}</p>
    <p><strong>Offer description </strong>: {description}</p>
    
    <div> <h3>Product</h3> </div>
    <p>End use: {end_use}</p>
    <p>Product duration: {period}</p>
    <p>Data Update Frequency: {frequency}</p>
    <p>Product Target: {target}</p>
    <p>Named Schemas Attributes targeted: {ns_attributes}</p>
    <p>Terms and Conditions: {terms_conditions}</p>
    
    <div> <h3>Price</h3> </div>
    <p>Monetization Engine: {monetization_engine}</p>
    <p>Payment Terms: {payment_terms}</p>
    <p>Price: {price}</p>
    <p>Shared Custody Terms: {share_custody_tc}</p>
    <p>Delivery : {delivery}</p>
    
    <div> <h3>Place</h3> </div>
    <p>Region: {region}</p><div>
    
    <h3>Promotion</h3>
    </div>
    <p>This offer is valid for the next: {offer_duration}</p>
    <p>Offer Promoted: {offer_promotion}</p>
    <p>Offer Front-end: HTML</p>"""
    
    period = period.get("unit") + str(period.get("value"))
    frequency = "Every " + str(frequency.get("value")) + frequency.get("unit").upper()
    try:
        target = target.get("targeted").captalize()
    except:
        pass
    
    empty = ""
    for i in ns_attributes:
        try:
            empty = i.captalize() + ", " + empty
        except:
            empty = i + ", " + empty
    del ns_attributes
    ns_attributes = empty[0:-2]
    price = price.get("unit") + str(price.get("value"))
    region = "Brazil" if region == "br" else region.upper()
    offer_duration = str(offer_duration.get("value")) + str(offer_duration.get("unit"))
    
    # html = html.replace("\n", "")
    return html.format(div_a = div_a, offer_name = offer_name.capitalize(), offer_category = offer_category.capitalize(), creator_id = creator_id.capitalize(), description = description.capitalize(), end_use = end_use.capitalize(), period = period, frequency = frequency, target = target, ns_attributes = ns_attributes, terms_conditions = terms_conditions.capitalize(), monetization_engine = monetization_engine.capitalize(), payment_terms = payment_terms.capitalize(), price = price, share_custody_tc = share_custody_tc.capitalize(), delivery = delivery.capitalize(), region = region, offer_duration = offer_duration, offer_promotion = offer_promotion.capitalize())

def join_offer_html(offer_list):
    of_key = list(offer_list.keys())
    
    html = """
    <div style='margin-top:5.0pt;margin-right:0cm;margin-bottom:10.0pt;margin-left:0cm;line-height:115%;font-size:13px;font-family:"Aptos",sans-serif;border:solid #156082 3.0pt;padding:0cm 0cm 0cm 0cm;background:#156082;'>
    <h1 style='margin-top:5.0pt;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:115%;background:#156082;border:none;padding:0cm;font-size:15px;font-family:"Aptos",sans-serif;color:white;font-weight:normal;text-align:center;'><strong><span style="font-size: 20px;">Offers</span></strong></h1>
</div>
    """
    end = """ <div style='margin-top:5.0pt;margin-right:0cm;margin-bottom:10.0pt;margin-left:0cm;line-height:115%;font-size:13px;font-family:"Aptos",sans-serif;border:none;border-top:solid #156082 1.0pt;padding:2.0pt 0cm 0cm 0cm;'> </div><p><br></p>"""

    for i in of_key:
        html = html + offer_html(offer_name = offer_list[i][i].get("offer_name"), offer_category = offer_list[i][i].get("product").get("offer_category"), creator_id = offer_list[i][i].get("creator_id"), 
                                  description = offer_list[i][i].get("product").get("description"), end_use = offer_list[i][i].get("product").get("end_use"), 
                                period = offer_list[i][i].get("product").get("period"), frequency = offer_list[i][i].get("product").get("frequency"), target = offer_list[i][i].get("product").get("target"), 
                                ns_attributes = offer_list[i][i].get("product").get("ns_attributes"), terms_conditions = offer_list[i][i].get("product").get("terms_conditions"), 
                                monetization_engine =  offer_list[i][i].get("price").get("monetization_engine"), payment_terms = offer_list[i][i].get("price").get("payment_terms"), price = offer_list[i][i].get("price").get("price") , share_custody_tc = offer_list[i][i].get("price").get("share_custody_tc"), 
                                delivery = offer_list[i][i].get("price").get("delivery"), region = offer_list[i][i].get("place").get("region"), offer_duration  = offer_list[i][i].get("promotion").get("offer_duration"), offer_promotion = offer_list[i][i].get("promotion").get("offer_promotion")) + "<p><br></p>" + end

    return html.replace("\n", "") + "</html>"

def dt_to_html(df):
    font_type = 'Myriad Pro Light'
    df = df
    n_rows = df.shape[0]
    n_cols = df.shape[1]

    title = ""
    for i in range(n_cols):
        title = title + "<td> <p align='center'> <strong>" + df.columns[i] + "</strong>  </p> </td>"

    title = "<tr style='background-color:#EC6623;'>" + title + "</tr>"

    body = ''
    for i in range(n_rows):
        body = body + "<tr>"

        for j in range(n_cols):
            body = body + "<td width='132' nowrap='' valign='bottom''> <p align='left'>" + str(
                df.iloc[i, j]) + "</p> </td>"

        body = body + "</tr>"

    structure_html = """
                    <style>
                            div.texto_comum {
                              margin-top:0cm;
                              margin-right:0cm;
                              margin-bottom:8.0pt;
                              margin-left:0cm;
                              line-height:107%;
                              font-size:15px;
                              font-family:""" + font_type + """sans-serif;
                            }
                    </style>

                    <table border='1' cellspacing='0' cellpadding='0'>
                        <tbody>
                              <div class= 'texto_comum'>
                              """ + title + body + """
                            </div>
                              </tbody>
                              </table>"""

    table = structure_html
    return table
    
def dsp_html(plan_info, calc_dicty, members_full_df):
    plan_name = list(plan_info.keys())[0]
    start_date = plan_info.get(plan_name).get('start_date')
    payment_freq_M = plan_info.get(plan_name).get('payment_freq_M')
    ns_list = plan_info.get(plan_name).get('ns')
    ns = ""
    for i in ns_list:
        ns = ns +i.upper() + ", "
    ns = ns[:-2]
    
    # table = dt_to_html(calc_dicty.get('members_df')).replace("\n", "")
    table1 = calc_dicty.get('members_df')[['dw_id', 'name', 'ns', 'N', 'DIM']].drop_duplicates()
    if members_full_df:
        table2 = calc_dicty.get('members_df')
        table2 = table2.drop(['ns', 'N', 'DIM'], axis=1).drop_duplicates()
        table2.columns = ['DrumWave Id', 'Member Name', 'ID Category', 'ID Number', 'Gender', 'Age', 'Height','Weight', 'Address', 'City', 'State', 'Zip Code', 'Start Date', 'Offer Participated', 'Time in Plan (T)', 'Quota Calculation (Qa)', 'Payment Reveived ($)']
    else:
        table2 = calc_dicty.get('members_df')[['dw_id', 'name', 'start_date', 'o', 't', 'qa', 'cash']].drop_duplicates()
        table2.columns = ['DrumWave Id', 'Member Name', 'Start Date', 'Offer Participated', 'Time in Plan (T)', 'Quota Calculation (Qa)', 'Payment Reveived ($)']
        
    table2['Start Date'] = [str(i)[0:10] for i in table2['Start Date']]
    table2['Payment Reveived ($)'] = ['${:,.2f}'.format(i) for i in  table2['Payment Reveived ($)']]
    table2['Quota Calculation (Qa)'] = [round(i,4) for i in  table2['Quota Calculation (Qa)']]
    table2 = table2.sort_values('Payment Reveived ($)')
    # table.columns = ['DrumWave Id', 'Member Name', 'Start Date', 'Named Schema', 'N', 'DIM', 'Offer Participated', 'Time in Plan (T)' ]
    table1.columns = ['DrumWave Id', 'Member Name', 'Named Schema', 'N', 'DIM']
    table1 = table1.sort_values('Member Name')
    table1 = dt_to_html(table1).replace("\n", "")
    table2 = dt_to_html(table2).replace("\n", "")

    base_html = """ <html>
    <div style='margin-top:5.0pt;margin-right:0cm;margin-bottom:10.0pt;margin-left:0cm;line-height:115%;font-size:13px;font-family:"Aptos",sans-serif;border:solid #FFC000 3.0pt;padding:0cm 0cm 0cm 0cm;background:#FFC000;'>
    <h1 style='margin-top:5.0pt;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:115%;background:#FFC000;border:none;padding:0cm;font-size:15px;font-family:"Aptos",sans-serif;color:white;font-weight:normal;text-align:center;'><strong><span style="font-size: 20px; color: rgb(0, 0, 0);">
    {plan_name} Data Savings Plan</span></strong></h1>
    </div>
    <p><strong>id:&nbsp;</strong>{id_p}</p>
    <p><strong>Category:</strong> {category}</p>
    <p><strong>Available Named Schemas:</strong> {ns}</p>
    <p><strong>Plan Launched in:</strong> {start_date}</p>
    <p><strong>Initial Member Quotas (Qi)</strong>: {qi}</p>
    <p><strong>Total Quotas (Qt)</strong>: {qt}</p>
    <p><strong>Payment Methodology:&nbsp;</strong>{pay_method}</p>
    <p><strong>Payment Formula:&nbsp;</strong>{formula}</p>
    <p><strong>Payment Frequency:&nbsp;</strong>Every {payment_freq_M} M</p>
    
    &nbsp
    
    <div style='margin-top:5.0pt;margin-right:0cm;margin-bottom:10.0pt;margin-left:0cm;line-height:115%;font-size:13px;font-family:"Aptos",sans-serif;border:solid #ff9248 3.0pt;padding:0cm 0cm 0cm 0cm;background:#ff9248;'>
        <h1 style='margin-top:5.0pt;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:115%;background:#ff9248;border:none;padding:0cm;font-size:15px;font-family:"Aptos",sans-serif;color:white;font-weight:normal;text-align:center;'><span style="font-size: 20px; color: rgb(0, 0, 0);"><strong>Assumptions and Guidelines</strong></span></h1>
    </div>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;font-size:11.0pt;font-family:"Aptos",sans-serif;'>The primary objective of this experiment was to test which parameters should be considered when allocating resources of offers to users of a Data Saivngs Plan</p>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;font-size:11.0pt;font-family:"Aptos",sans-serif;'>Thus, let&rsquo;s assume that:</p>
    <ul style="list-style-type: disc;">
    <li>Qi = Initial Quota that a user receives when entering a Data Savings Plan (DSP)</li>
    <li>t = timeframe in months</li>
    <li>Ot = Number of Offers in period t</li>
    <li>Qt = Total Quota of all participants in the DSP</li>
    <li>Qat = Quota attribution in period t</li>
    <li>O = Total number of offers in which a user participates in period t</li>
    <li>Mt = Total pool of money from offers received in period t</li>
    <li>T = Time in months since the participant has entered the plan</li>
    <li>Nt = Total number of contributions that a user has from all Named Schemas (NS) in a DSP</li>
    <li>PT = Weight of time (T) in the equation</li>
    <li>DIMt = Average DIM score from all NS in the DSP</li>
    </ul>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;font-size:11.0pt;font-family:"Aptos",sans-serif;'><strong>Note:</strong> Nt and DIMt are only updated when the user participates (automatically) in an offer where that targets one&rsquo;s named schema.</p>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;font-size:11.0pt;font-family:"Aptos",sans-serif;'><u>Example to explain this note</u>:&nbsp;</p>
    <ul>
    <li style="margin-top: 0cm; margin-right: 0cm; margin-bottom: 8pt; font-size: 11pt; font-family: Aptos, sans-serif;">User: Jake</li>
    <li style="margin-top: 0cm; margin-right: 0cm; margin-bottom: 8pt; font-size: 11pt; font-family: Aptos, sans-serif;">Period 1<ul>
            <li style="margin-top: 0cm; margin-right: 0cm; margin-bottom: 8pt; font-size: 11pt; font-family: Aptos, sans-serif;">Jake N<sub>1&nbsp;</sub>= 3 and DIM<sub>1</sub> = 4</li>
        </ul>
    </li>
    <li style="margin-top: 0cm; margin-right: 0cm; margin-bottom: 8pt; font-size: 11pt; font-family: Aptos, sans-serif;">Period 2<ul>
            <li style="margin-top: 0cm; margin-right: 0cm; margin-bottom: 8pt; font-size: 11pt; font-family: Aptos, sans-serif;">There is a new offer an offer for credit card named schema (which Jake is eligible).&nbsp;</li>
            <li style="margin-top: 0cm; margin-right: 0cm; margin-bottom: 8pt; font-size: 11pt; font-family: Aptos, sans-serif;">When the offer occurs and the user&rsquo;s data is queried then the new information shows that<ul>
                    <li style="margin-top: 0cm; margin-right: 0cm; margin-bottom: 8pt; font-size: 11pt; font-family: Aptos, sans-serif;">There are 6 new contributions</li>
                    <li style="margin-top: 0cm; margin-right: 0cm; margin-bottom: 8pt; font-size: 11pt; font-family: Aptos, sans-serif;">the DIM score of this named schema is equal to 8</li>
                </ul>
            </li>
            <li style="margin-top: 0cm; margin-right: 0cm; margin-bottom: 8pt; font-size: 11pt; font-family: Aptos, sans-serif;">Jake N<sub>2</sub> = 3 + 6 = 9 and DIM<sub>2</sub> = (4 + 8)/2 = 6</li>
        </ul>
    </li>
    </ul>
    &nbsp
    
    {offer_html}
    
    <div style='margin-top:5.0pt;margin-right:0cm;margin-bottom:10.0pt;margin-left:0cm;line-height:115%;font-size:13px;font-family:"Aptos",sans-serif;border:solid #7CFC00 3.0pt;padding:0cm 0cm 0cm 0cm;background:#7CFC00;'>
        <h1 style='margin-top:5.0pt;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:115%;background:#7CFC00;border:none;padding:0cm;font-size:15px;font-family:"Aptos",sans-serif;color:white;font-weight:normal;text-align:center;'><span style="font-size: 20px; color: rgb(0, 0, 0);"><strong>Results</strong></span></h1>
    </div>
    <p><strong>Total number of offers (O)</strong>: {o}</p>
    <p><strong>Total Revenue from Offers (M)</strong>: {m} USD</p>
    <p><strong>Distribution Date</strong>: {dist_date}</p>
    <p><strong>Members</strong></p>
    &nbsp
    {table1}
    &nbsp
    {table2}
    
    &nbsp
    <h1 <style = color:#FF0000>Please see Graphs in attachments</h1>
    <p><br></p>
        """
    base_html = base_html.format(plan_name = plan_name.capitalize(), id_p = plan_info.get(plan_name).get('id'), 
                                  category = plan_info.get(plan_name).get('category').capitalize(), ns = ns, start_date = start_date, payment_freq_M = payment_freq_M, 
                                  o = calc_dicty.get('members_df')[["o"]].max()[0],  m = '${:,.2f}'.format(calc_dicty.get('m')),
                                  pay_method = calc_dicty.get('pay_formula').capitalize(), formula = calc_dicty.get('formula'), offer_html = calc_dicty.get('offer_html'),
                                  dist_date = str(datetime.strptime(start_date, '%Y-%m-%d') + relativedelta(months=payment_freq_M))[:10], qt = calc_dicty.get('qt'), 
                                  qi = calc_dicty.get('qi'), table1 = table1, table2 = table2)
    return base_html

def send_html_email(to_email, subject, html_content, attachment_path):
    ## Email
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    # from email.mime.image import MIMEImage

    # Your email credentials
    sender_email = 'jucalecrim@outlook.com'
    sender_password = 'RBravo@@0'

    # Create the MIMEMultipart object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    
    
    # Attach the file as an attachment
    attachment = open(attachment_path, 'rb')
    base = MIMEBase('application', 'octet-stream')
    base.set_payload((attachment).read())
    encoders.encode_base64(base)
    base.add_header('Content-Disposition', 'attachment; filename = %s' % attachment_path.split('/')[-1])
    message.attach(base)

    # Attach the HTML content to the email
    html_body = MIMEText(html_content, 'html')
    message.attach(html_body)


    # SMTP connection and sending the email
    try:
        with smtplib.SMTP("smtp-mail.outlook.com", port=587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
            server.quit()
            # import os
            # os.remove(attachment_path)
        return 200
    except Exception as exe:
        print(exe)
        return 500

def monetize_dsp(dsp = 'open health', start_date = '2023-01-01', members_start_date_random = True, members_full_df = False, random_N = True, random_DIM = True,
                  n_members = 0, calculation_method = 'alfa', offer_n = 0, offer_p_random = True, min_offer_p = 1000, qi = 100, pt = 0.75,
                  receiver_email = 'jucaluis@gmail.com'):

    # import azure.functions as func
    # import base64
    
    name_df = pd.DataFrame(name_dataset(name_list = name_generator(size=n_members, gender = 'random')))
    
    if dsp == 'open health':
        plan_info = {"open health":{"id":"HC_001","category":"health care", 
                                    "ns":["CBC", "CEA", "GL"], 
                                    'start_date':'2023-01-01', #string format YMD
                                    'payment_freq_M':12}} #"Blood Sample","Mamography","X-Ray","Eye Exam", "Brain Scan"
    elif dsp == 'open finance':
        plan_info = {"open finance":{"id":"OF_001","category":"finance", 
                                      "ns":["cc_fatura", "cc_conta_pagamento", "limites", "transacoes", "relacoes_fin"], 
                                      'start_date':'2023-01-01', 
                                      'payment_freq_M':6  }}
    else:
        plan_info = dsp
    
    plan_ds = plans(2, plan_info)
        
    df_full2 = name_df.merge(fill_db(members = list(name_df['name'].unique()), plan_info = plan_info, start_date = start_date, start_date_random = members_start_date_random, random_N = random_N, random_DIM = random_DIM), how = 'left', on = 'name')
    df_full2 = df_full2.dropna()
    del name_df

    offer_list = offer_loop(plan_info, length = offer_n, rand_price = offer_p_random, price = min_offer_p) 

    calc_dicty = dist_calculation(plan_info = plan_ds, offers = offer_list, member_ns_df = df_full2, qi = qi, pt = pt, method = calculation_method)
    
    offer_htmls = join_offer_html(offer_list)
    calc_dicty['offer_html'] = offer_htmls        
    
    from tempfile  import gettempdir
    dir_temp = gettempdir() + '\\img.jpg'
    # dir_temp = gettempdir() + '\\img.html'
    
    plot_return = plot_graph(qa_df = calc_dicty.get('qa_df').sort_values('cash'), path = dir_temp, n_bars = 10)
    print(plot_return)

    plan_html = dsp_html(plan_info, calc_dicty, members_full_df)
    
    a = send_html_email(to_email = receiver_email, subject = list(plan_info.keys())[0].upper() + "Data Savings Plan" , html_content = plan_html, attachment_path = dir_temp)    
    return a


from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from pydantic import BaseModel
import json

app = FastAPI()

class DSP_structure(BaseModel):
    dsp: str = 'open health'
    start_date: str ='2023-01-01'
    members_start_date_random: bool = True
    members_full_df: bool = False
    random_N: bool = True
    random_DIM: bool = True
    n_members: Optional[int] = 0 #0 is random
    calculation_method: str = 'alfa'
    offer_n: Optional[int] = 0
    offer_p_random: bool = True
    min_offer_p: int = 1000
    qi: int = 100
    pt: float = 0.75
    receiver_email:str = 'youremail@drumwave.com'
    
    
@app.post("/dsp_email_sender")
def dsp_email_response(item: DSP_structure):
    try:
        
        result = monetize_dsp(dsp = item.dsp, start_date = item.start_date, members_start_date_random = item.members_start_date_random, members_full_df = item.members_full_df, 
                              random_N = item.random_N, random_DIM = item.random_DIM,
                      n_members = item.n_members, calculation_method = item.calculation_method, offer_n = item.offer_n, offer_p_random = item.offer_p_random, min_offer_p = item.min_offer_p,
                      qi = item.qi, pt = item.pt, receiver_email = item.receiver_email)
        print(result)
        
        return HTTPException(status_code=200, detail="Deu BOM")
    except Exception as exe:
        return HTTPException(status_code=404, detail="ERRO MALUCO {}".format(exe))

    
@app.get("/name_generator")
def random_name_generator(size: int, gender: str = 'random'):
    try:
        output = name_generator(size = size, gender = gender)
        # print(type(output))
        return HTTPException(status_code=200, detail="Deu BOM receba seus abaixo", headers=output)
    except Exception as exe:
        return HTTPException(status_code=404, detail="ERRO nos nomes {}".format(exe))
    
@app.post("/name_dataset")
def random_name_dataset(name_list: list = name_generator(size = 2, gender = 'random')):
    try:
        # name_list = name_list.split(",")
        # name_list = [i.strip().capitalize() for i in name_list]
        output = name_dataset(name_list = name_list)
        return HTTPException(status_code=200, detail="Deu BOM receba seu DF", headers= pd.DataFrame(output).to_json(orient = 'index'))
    except Exception as exe:
        return HTTPException(status_code=404, detail="ERRO nos nomes {}".format(exe))

@app.get("/quota_calculator")
def calc_individual_quota(o: int, n: int, t:int, dim:float, qi:int, qt:float, pt:float, method:str = 'alfa'):
    try:
        output = quota_calculator(o, n, t, dim, qi, qt, pt)
        return HTTPException(status_code=200, detail="Qa = {}".format(round(output, 5)), headers= round(output, 8))
    except Exception as exe:
        return HTTPException(status_code=404, detail="ERRO calculando quotas {}".format(exe))


class members_structure(BaseModel):
    members: list = ["Your name", "My name"]
    plan_info: dict = {"open health":{"id":"HC_001","category":"health care", 
                                  "ns":["Blood Test", "Glicose Level", "Mamography", "X-Ray"], 
                                  'start_date':'2022-01-01', 
                                  'payment_freq_M':12  }}

    
@app.post("/fill_db")
def members_database(items: members_structure, start_date: str = 'YYYY/MM/DD', start_date_random:bool = True, random_N: bool = True, random_DIM: bool = True): #erro quando a data é diferente de 2023/01/01
    try:
        start_date = "2023-01-01" if start_date == 'YYYY/MM/DD' else start_date #ERRO na DATA
        output = fill_db(members = items.members, plan_info = items.plan_info, start_date = datetime.strptime(start_date, "%Y-%m-%d"), start_date_random = start_date_random, random_N = random_N, random_DIM = random_DIM)
        print(output.head())
        return HTTPException(status_code=200, detail="Deu BOM receba seu DF", headers= pd.DataFrame(output).to_json(orient = 'index'))
    except Exception as exe:
        return HTTPException(status_code=404, detail="ERRO formando db {}".format(exe))
    
    
@app.get("/sp_stocks")
def get_stocks():
    try:
        return HTTPException(status_code=200, detail="Here are your stocks: ", headers = pd.DataFrame(sp_stocks()).to_json(orient = "index"))
    except Exception as exe:
        return HTTPException(status_code=404, detail="ERROR getting stocks {}".format(exe))

class off_info(BaseModel):
    company_info: dict = {'ticker':"ITUB4", 'company':'Itau Unibanco', 'industry':"Finance"}
    ns_list: list = ['fatura_cartao', 'credito_consignado', 'despesas_restaurante']

@app.post("/generate_offers")
def random_offers(items: off_info, dsp_target: str = 'open health', price: float = float(100.00), offer_creation_date: str = 'YYYY/MM/DD'):
    try:
        offer_creation_date = "2024-01-01" if offer_creation_date == "YYYY/MM/DD" else offer_creation_date
        output = random_offer_generator(company_info = items.company_info, ns_list = items.ns_list, dsp_target = dsp_target, price =price, offer_creation_date = offer_creation_date)
        return HTTPException(status_code=200, detail="Here is your offer: ", headers = json.dumps(output, indent=4))
    except Exception as exe:
        return HTTPException(status_code=404, detail="No offers for you my friend =( {}".format(exe))
    
    
@app.post('/multiple_offer_loop')
def off_loop(plan_info: dict, length: int = 5, rand_price: bool = True, price:int = 100):
    try:
        output = offer_loop(plan_info = plan_info, length = length, rand_price = rand_price, price = price)
        return HTTPException(status_code=200, detail="Here are your offers: ", headers = output)
    except Exception as exe:
        print(exe)
        return HTTPException(status_code=404, detail="ERRO this loop ain't working sorry {}".format(exe))

class PLT_structure(BaseModel):
    qa_df: dict = {
                    "name": [
                      "You",
                      "Me",
                      "Us",
                      "Them",
                      "Drumwave team US",
                      "DrumWave team BR"
                    ],
                    "cash": [50.50, 200.72, 700.20, 500.44, 300.97, 340.74]
                  }
    path: str = "C:\\user\\img.png"
    n_bars: Optional[int] = 5
    
@app.post('/plot_g')
def plt_graph(items: PLT_structure):
    try:
        qa_df = pd.DataFrame(items.qa_df)
        output = plot_graph(qa_df, items.path, items.n_bars)
        return HTTPException(status_code=200, detail="Here is your graph: ", headers = output)
    except Exception as exe:
        print(exe)
        return HTTPException(status_code=404, detail="ERROR no graph for you my friend {}".format(exe))

class Qa_Dist_Calc(BaseModel):
    plan_info: dict = {"open health": {"id": "HC_001", "category": "health care", "ns": ["Blood Test", "Glicose Level", "Mamography", "X-Ray"], "start_date": "2022-01-01","payment_freq_M": 12}}
    offers: dict = {'A_1': {'A_1': {'creator_id': 'A__DW',  'offer_name': 'Offer Example', 'creation_date': '2023-4-1', 'product': {'offer_category': 'buy', 'offer_type': 'dsp', 'description': 'descript','end_use': 'BRD','period': {'unit': 'M', 'value': 4}, 'frequency': {'unit': 'H', 'value': 36},'target': 'public','ns_attributes': ['GL'], 'terms_conditions': 'XXX'}, 'price': {'monetization_engine': 'cash_now', 'payment_terms': 'upfront', 'price': {'unit': 'BRL', 'value': 100}, 'share_custody_tc': '50%/50% ', 'delivery': 'virtual'}, 'place': {'region': 'br'}, 'promotion': {'offer_duration': {'unit': 'D', 'value': 6},'offer_promotion': 'False','front_end': ''}}},
     'B_1': {'B_1': {'creator_id': 'B__DW', 'offer_name': 'Offer 2','creation_date': '2023-1-1', 'product': {'offer_category': 'sell', 'offer_type': 'dsp','description': 'Descript', 'end_use': 'licensing','period': {'unit': 'M', 'value': 8}, 'frequency': {'unit': 'RT', 'value': 1},'target': {'targeted': 'open finance'}, 'ns_attributes': ['cc'],'terms_conditions': 'XXXXXXX'}, 'price': {'monetization_engine': 'cash_now', 'payment_terms': 'upfront', 'price': {'unit': 'BRL', 'value': 10000}, 'share_custody_tc': '50%/50%', 'delivery': 'virtual'},'place': {'region': 'us'}, 'promotion': {'offer_duration': {'unit': 'H', 'value': 8},'offer_promotion': 'False', 'front_end': ''}}}}
    member_ns_df: dict = {'dw_id': {0: 'ED_001', 1: 'ED_001', 2: 'ED_001', 3: 'EM_001', 4: 'EM_001'},
     'name': {0: 'Edna Wallace',
      1: 'Edna Wallace',
      2: 'Edna Wallace',
      3: 'Emily Odonnell',
      4: 'Emily Odonnell'},
     'id_type': {0: 'RG', 1: 'RG', 2: 'RG', 3: 'RG', 4: 'RG'},
     'id_number': {0: '15.582.333-02',
      1: '15.582.333-02',
      2: '15.582.333-02',
      3: '67.730.146-84',
      4: '67.730.146-84'},
     'gender': {0: 'female', 1: 'female', 2: 'female', 3: 'female', 4: 'female'},
     'age': {0: 81, 1: 81, 2: 81, 3: 52, 4: 52},
     'height': {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.12, 4: 1.12},
     'weight': {0: 100, 1: 100, 2: 100, 3: 52, 4: 52},
     'address': {0: '4632 Vermont 15',
      1: '4632 Vermont 15',
      2: '4632 Vermont 15',
      3: '40902 Ingersoll Terrace',
      4: '40902 Ingersoll Terrace'},
     'city': {0: 'Wolcott',
      1: 'Wolcott',
      2: 'Wolcott',
      3: 'Fremont',
      4: 'Fremont'},
     'state': {0: 'VT', 1: 'VT', 2: 'VT', 3: 'CA', 4: 'CA'},
     'zip': {0: '05680', 1: '05680', 2: '05680', 3: '94538', 4: '94538'},
     'start_date': {0: '2023-02-01',
      1: '2023-02-01',
      2: '2023-04-01',
      3: '2023-04-01',
      4: '2023-12-01'},
     'ns': {0: 'CBC', 1: 'CEA', 2: 'GL', 3: 'CBC', 4: 'CEA'},
     'N': {0: 50, 1: 34, 2: 73, 3: 7, 4: 53},
     'DIM': {0: 7, 1: 5, 2: 5, 3: 5, 4: 7}}
    qi: int = 100
    pt:float = 0.75
    method: str = 'alfa'
    
@app.post('/dsp_distribution_calc')
def dist_calc(items: Qa_Dist_Calc):
    try:

        member_ns_df = pd.DataFrame(items.member_ns_df)

        member_ns_df['start_date'] = [datetime.strptime(i, "%Y-%m-%d") for i in member_ns_df['start_date']]

        output = dist_calculation(items.plan_info, items.offers, member_ns_df, items.qi, items.pt, items.method)
        qa2 = output['qa_df']
        mdf2 = output['members_df']
        output.update({'qa_df':qa2.to_dict(), 'members_df':mdf2.to_dict()})
        # return HTTPException(status_code=200, detail="Here is your calculation distribution dictionary: ", headers = json.dumps(output, indent = 4))
        return HTTPException(status_code=200, detail="Here is your calculation distribution dictionary: ", headers = output)
    except Exception as exe:
        print(exe)
        return HTTPException(status_code=404, detail="ERROR now =( {}".format(exe))
    
class df_html_class(BaseModel):
    df: dict = {'name':{0: 'Edna Wallace',
      1: 'Edna Wallace',
      2: 'Edna Wallace',
      3: 'Emily Odonnell',
      4: 'Emily Odonnell'},
     'id_number': {0: '15.582.333-02',
      1: '15.582.333-02',
      2: '15.582.333-02',
      3: '67.730.146-84',
      4: '67.730.146-84'},
     'gender': {0: 'female', 1: 'female', 2: 'female', 3: 'female', 4: 'female'},
     'age': {0: 81, 1: 81, 2: 81, 3: 52, 4: 52},
     'zip': {0: '05680', 1: '05680', 2: '05680', 3: '94538', 4: '94538'},
     'ns': {0: 'CBC', 1: 'CEA', 2: 'GL', 3: 'CBC', 4: 'CEA'},
     'DIM': {0: 7, 1: 5, 2: 5, 3: 5, 4: 7}}
    qi: int = 100
    pt:float = 0.75
    method: str = 'alfa'
    
@app.post('/df_to_html')
def df_to_html(items: df_html_class):
    try:
        df = pd.DataFrame(items.df)
        output = dt_to_html(df).replace("\n", "")
        return HTTPException(status_code=200, detail="Here is your table html as a string: ", headers = output)
    except Exception as exe:
        print(exe)
        return HTTPException(status_code=404, detail="ERROR no html buddy {}".format(exe))
    
class def_html(BaseModel):
    plan_info: dict = {'open health': {'id': 'HC_001', 'category': 'health care','ns': ['CBC', 'CEA', 'GL'],  'start_date': '2023-01-01',  'payment_freq_M': 12}}
    calc_dicty: dict = {'qa_df':{'name': {0: 'Elizabeth Irving', 1: 'Dustin Alexander', 2: 'Nelda Hatcher'}, 'qa': {0: 0.13, 1: 0.59, 2: 0.66}, 'cash': {0: 108.68, 1: 480.86, 2: 539.21}},
                        'm':10000, 'qi':100, 'qt':10000, 'pt':0.75, 'formula':'(((Qt * T)*Pt + N*DIM*(1-Pt))*(1+O))/Qt = Standard Base LiNe Formula', 'pay_formula':'alfa',
                        'members_df':{'dw_id': {0: 'EL_001', 1: 'EL_001', 2: 'DU_001'},
                             'name': {0: 'Elizabeth Irving', 1: 'Elizabeth Irving', 2: 'Dustin Alexander'},
                             'id_type': {0: 'RG', 1: 'RG', 2: 'RG'},
                             'id_number': {0: '41.071.082-03', 1: '41.071.082-03', 2: '41.730.754-84'},
                             'gender': {0: 'female', 1: 'female', 2: 'female'},
                             'age': {0: 47, 1: 47, 2: 18},
                             'height': {0: 1.0, 1: 1.0, 2: 1.9},
                             'weight': {0: 94, 1: 94, 2: 100},
                             'address': {0: '10340 West 62nd Place',
                              1: '10340 West 62nd Place',
                              2: '34 Belair Drive'},
                             'city': {0: 'Arvada', 1: 'Arvada', 2: 'Holbrook'},
                             'state': {0: 'CO', 1: 'CO', 2: 'MA'},
                             'zip': {0: '80004', 1: '80004', 2: '02343'},
                             'start_date': {0: '2023-02-01',
                              1: '2023-02-01',
                              2: '2023-03-01'},
                             'ns': {0: 'CBC', 1: 'GL', 2: 'CBC'},
                             'N': {0: 20, 1: 11, 2: 66},
                             'DIM': {0: 5, 1: 9, 2: 9},
                             'o': {0: 4, 1: 4, 2: 4},
                             't': {0: 2, 1: 2, 2: 2},
                             'qa': {0: 0.133, 1: 0.13, 2: 0.59},
                             'cash': {0: 108.68, 1: 108.67, 2: 480.85}},
                        'offer_html':'<html><p>HTML Example: Offers </p></html>'}
                        
                        
    
@app.post('/datasavings_html')
def ds_html(items: def_html, members_full_df: bool = False):
    try:
        calc_dicty = items.calc_dicty
        members_df = pd.DataFrame(calc_dicty.get("members_df"))
        members_df['start_date'] = [datetime.strptime(i, "%Y-%m-%d") for i in members_df['start_date']]
        calc_dicty.update({"qa_df":pd.DataFrame(calc_dicty.get("qa_df")), "members_df":members_df})
        
        output = dsp_html(items.plan_info, calc_dicty, members_full_df)
        output = output.replace("\n", "")
        return HTTPException(status_code=200, detail="OK here is you loooong HTML", headers = output)
    except Exception as exe:
        print(exe)
        return HTTPException(status_code=404, detail="ERROR generating your DSP HTML due to {}".format(exe))


##TO-DO
#publicar a API - ver vídeo

#intro deck 5 slides
#deck de apresentação pra 1 hora (11 slides) - falar 20 min e o resto responder pergunta
#full deck pos reunião - via doc send precisa mais de 20 slides
#reuniao de deal flow - 
#Q&A - 
#IC - investors commitee - GO/No Go
