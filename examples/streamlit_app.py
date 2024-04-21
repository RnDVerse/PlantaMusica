from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Planta Musica!

Edit `/plantamusica.py` to customize this app and add more features or functionalities

If you have any questions, checkout our [documentation](https://docs.plantamusica.cloud) and [community
forums](https://discuss.plantamusica.cloud).

In the meantime, below is an example of what you can do with the current Planta Musica App:
"""

with st.echo(code_location='below'):
   total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
   num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

   Point = namedtuple('Point', 'x y')
   data = []

   points_per_turn = total_points / num_turns

   for curr_point_num in range(total_points):
      curr_turn, i = divmod(curr_point_num, points_per_turn)
      angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
      radius = curr_point_num / total_points
      x = radius * math.cos(angle)
      y = radius * math.sin(angle)
      data.append(Point(x, y))

   st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
      .mark_circle(color='#0068c9', opacity=0.5)
      .encode(x='x:Q', y='y:Q'))
