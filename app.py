import streamlit as st
import pandas as pd
from src.recommend import recommend_similar

st.set_page_config(
    page_title="Spotify Recommender", 
    page_icon="🎵", 
    layout="centered"
)

if 'current_song' not in st.session_state:
    st.session_state.current_song = ""

st.markdown(
    """
    <h1 style='white-space: nowrap; font-size: 2.4rem; overflow: hidden; text-overflow: ellipsis;'>
        🎵 Spotify Recommendation System
    </h1>
    """, 
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color: #b3b3b3; font-size: 1.1rem; margin-bottom: 2rem;'>"
    "Discover your next favorite track based on the music you already love.</p>", 
    unsafe_allow_html=True
)

song_input = st.text_input("Search for a track...", value=st.session_state.current_song, placeholder="e.g., Bohemian Rhapsody")

if song_input and song_input != st.session_state.current_song:
    st.session_state.current_song = song_input

if st.session_state.current_song:
    with st.spinner("Finding similar tracks..."):
        results = recommend_similar(st.session_state.current_song)
    
    if isinstance(results, pd.DataFrame):
        items = results.to_dict('records')
    else:
        items = items

    if items is not None:
        filtered_items = []
        search_query_lower = st.session_state.current_song.strip().lower()
        
        for item in items:
            if isinstance(item, dict):
                track_name = item.get('name', item.get('track', item.get('title', 'Unknown Track')))
            else:
                track_name = str(item)
            
            if track_name.strip().lower() != search_query_lower:
                filtered_items.append(item)
        
        items = filtered_items[:5]

    if items is not None and len(items) > 0:
        first_item = items[0]

        mood_messages = {
            "Balanced": "Balanced vibes today! 🎧",
            "Party": "You're in a party mood! 🎉",
            "Chill": "You feeling chill today? 🛋️",
            "Workout": "Ready for a workout? 💪",
            "Energetic": "You're feeling energetic today! ⚡"
        }

        mood_text = f"Recommended based on: {st.session_state.current_song}"
        
        if isinstance(first_item, dict):
            cluster_name = first_item.get('cluster_name')

            
            if cluster_name is not None and cluster_name in mood_messages:
                mood_text = f"{mood_messages[cluster_name]} (Based on: {st.session_state.current_song})"
            elif cluster_name is not None:
                mood_text = f"Vibe: {cluster_name} 🎶 (Based on: {st.session_state.current_song})"

        st.subheader(mood_text)
        
        cols = st.columns(3) 
        for i, item in enumerate(items):
            with cols[i % 3]:
                if isinstance(item, dict):
                    track_name = item.get('name', item.get('track', item.get('title', 'Unknown Track')))
                    
                    artist_raw = item.get('artists', item.get('artist', 'Unknown Artist'))
                    if isinstance(artist_raw, str):
                        artist_name = artist_raw.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
                    elif isinstance(artist_raw, list):
                        artist_name = ", ".join(artist_raw)
                    else:
                        artist_name = str(artist_raw)
                else:
                    track_name = str(item)
                    artist_name = ""

                st.markdown(f"""
                <div style="
                    background-color: #181818; 
                    padding: 20px; 
                    border-radius: 8px 8px 0 0; 
                    margin-top: 15px; 
                    height: 100px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <h4 style="margin:0; padding:0; color:#FFFFFF; font-size: 1rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{track_name}">{track_name}</h4>
                    <p style="margin:5px 0 0 0; padding:0; color:#B3B3B3; font-size: 0.85rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{artist_name}">{artist_name}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🎧 Explore Similar", key=f"btn_{track_name}_{i}", use_container_width=True):
                    st.session_state.current_song = track_name
                    st.rerun()
    else:
        st.warning("No recommendations found for this track. Try another one!")