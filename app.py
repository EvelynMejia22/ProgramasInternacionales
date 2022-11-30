import requests
import base64
import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
import time
from streamlit_option_menu import option_menu

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

DATA_URL= 'internacional.csv'
df = px.pd.read_csv(DATA_URL)
df3 = px.pd.read_csv(DATA_URL)

@st.cache
def load_data(nrows):
    data=pd.read_csv(DATA_URL, nrows=nrows)
    return data

data = load_data(1000)



#This code helps to hide the main menu of Streamlit
hide_st_style = """
			<style>
			#MainMenu {visibility: hidden;}
			footer {visibility: hidden;}
			header {visibility: hidden;}
			</style>
			"""
st.markdown(hide_st_style, unsafe_allow_html=True)


#------- Navigation Menu ----------
selected = option_menu(
	menu_title = None,
	options=["Home", "Study Programs", "Around the World", "Students per school", "Contact"],
	icons=["house", "book","globe2","trophy", "person"],
	orientation="horizontal",
)


if selected == "Home":
	# Here is the first section
    st.header("About IP :earth_americas:")
    st.write(
        """
        Programs abroad offer unique experiences and the opportunity to get to know different cultures and discover that there are many more common points than differences.\n
    That is why, as part of the internationalization strategy, they have worked in solid relationships with hundreds of universities around the world. To date, they have more than 670 agreements with foreign universities in more than 45 countries.\n
    This dashboard of international programs will help us to know the status of students and test these hypotheses: \n    
        Do 96% of students who apply to an academic program abroad remain their first option? \n 
        Each period, 80% of the students internationalize via exchange and only 20% internationalize with a study abroad, certification, summer or winter?
        """
    )
    st.image('https://scontent.fntr6-3.fna.fbcdn.net/v/t1.6435-9/154075283_10158034823458601_8496221239349424301_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=e3f864&_nc_ohc=L2ysDqMgNMkAX9Ck96_&_nc_ht=scontent.fntr6-3.fna&oh=00_AfDtlYK2PG1KHiUTmBPuZZfWxJTaN5dagZuVIL9YfekbAw&oe=639DEACE')


if selected == "Study Programs":
    # Here is the second section
    st.header("Study Programs :blue_book:")
    st.write('''
	Tec de Monterrey is divided into schools of engineering, business, humanities, social sciences, architecture, medicine, 3 high school modalities (bicultural, multicultural and international) and others such as master's and doctoral degrees.\n
    In this graph you can see the number of students per school who applied for an international program, where the majority focuses on engineering and business with 11,288 and 9,870 students respectively.
    ''')
    st.plotly_chart(px.treemap(df3, path=["Escuela"], hover_name="Escuela", color="Escuela"))
    st.write(
        '''
        Of all the students who apply to an international program, **88% remain in their first choice**, whether it is an exchange or study abroad.\n
        This confirms that **our hypothesis** of whether 96% of the students who apply remain in their first option **is not true**. This may be due to average, level of English or the moment in which the application was made.\n  
            In this graph you can see the number of students who were accepted in their first choice and those who were not.
        '''
        )
    st.plotly_chart(px.histogram(df, x="DUMMIE SeleccióFOP",color="SelecciónFOP",hover_name='SelecciónFOP'))




if selected == "Around the World":
	# Here is the third section
    st.header("Countries with the highest number of students per exchange or study abroad :earth_asia::round_pushpin:")
    st.write('''
		In this case, we are interested in seeing the countries to which the students go the most, since this will help us to balance the agreements that are in place or even eliminate some where there is not the expected demand.\n 
        In this graph you can see the number of students by country. Thus, Spain is the country with the most students abroad (6,942), followed by Canada (3,207) and France (3,170). \n 
    Those with fewer students are countries like Paraguay (2), Israel (15) and New Zealand (54).
	    ''')
    st.plotly_chart(px.choropleth(df, locations="CountryNames", color='Number',color_continuous_scale=px.colors.sequential.Viridis_r, projection='mollweide', hover_name='Country'))
    st.header("Number of students with academic excellence :mortar_board:")
    st.write('''
    Not all programs are open to all students, as shown in the following graph, there are programs of excellence where only students with an average greater than 95 apply. \n 
        In this graph you can see the number of students with academic excellence in each country. For example, Russia is an excellence exchange program so the students here have an average of 100 or in Indonesia the average is 97. 
    ''')
    st.plotly_chart(px.choropleth(df, locations="CountryNames", color='PERCENTILE90',color_continuous_scale=px.colors.diverging.Temps, projection='mollweide',hover_name='Country'))




#SANKEY DIAGRAM
df = px.pd.read_csv(DATA_URL)
def compute_region_tec(df): 
    if ('Norte' in df['Región TEC']):
        return 'Norte'
    elif ('Centro Sur' in df['Región TEC']):
        return 'Centro Sur'
    elif ('Ciudad de México' in df['Región TEC']): 
        return 'Ciudad de México'
    elif ('Occidente' in df['Región TEC']): 
        return 'Occidente'
    else:
        return 'Desarrollo Regional'
df['REGION'] = df.apply(compute_region_tec, axis = 1)
def compute_Continent(df): 
  if ('Europe' in df['Continent']):
        return 'Europe'
  elif ('America' in df['Continent']):
        return 'America'
  elif ('Asia' in df['Continent']): 
        return 'Asia'
  elif ('Africa' in df['Continent']): 
        return 'Africa'
  else:
      return 'Oceania'
df['CONTINENT'] = df.apply(compute_Continent, axis = 1)
def compute_ProgramType(df): 
  if ('Intercambio' in df['Program Type']):
        return 'Intercambio'
  else:
      return 'Study Abroad'
df['PROGRAMTYPE'] = df.apply(compute_ProgramType, axis = 1)


#SANKEY PROM ALUMNOS
df3 = px.pd.read_csv(DATA_URL)
def compute_ProgramType(df3): 
  if ('Intercambio' in df3['Program Type']):
        return 'Intercambio'
  else:
      return 'Study Abroad'
df3['PROGRAMTYPE'] = df3.apply(compute_ProgramType, axis = 1)

if selected == "Students per school":
    #Here is the fourth section
    st.header("Students per school :school:")
    st.write('''
    The following graph shows the preferences between exchange and study abroad in the different regions of the tec and the continent they prefer to go to, which, as we have already seen, is Europe.
    ''')
    st.plotly_chart(px.parallel_categories(df, dimensions=['REGION', 'PROGRAMTYPE', 'CONTINENT'],
            color="Number", color_continuous_scale=px.colors.diverging.Tealrose,
            labels={'REGION':'Tec Regions','PROGRAMTYPE':'Program Type','CONTINENT':'Continent'}))
    st.write(
            """
            In this graph you can see the number of students per Tec Region, per school and per program type.
            """
            )
    st.plotly_chart(px.sunburst(df, path=['Región TEC', 'Campus','Escuela', 'Program Type'], values='Number'))
    st.write("In the following graph, you can choose the school to find out the best averages within it and if that helps them stay in their first choice and the type of program that these averages tend to choose.")
    school_filter = st.selectbox("Select the School", pd.unique(df3["Escuela"]))
    df3 = df3[df3["Escuela"] == school_filter]
    st.plotly_chart(px.parallel_categories(df3, dimensions=['Escuela', 'BESTPROM', 'SelecciónFOP','PROGRAMTYPE'],
                color="Number", color_continuous_scale=px.colors.diverging.Tealrose,
                labels={'Escuela':'School','BESTPROM':'BestProm','SelecciónFOP':'FirstOp','PROGRAMTYPE':'Program Type'}))

    



# ---- CONTACT ----
if selected == "Contact":
    st.header("Get In Touch With Me! :raising_hand:")
    st.write("##")

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/YOUR@MAIL.COM" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)