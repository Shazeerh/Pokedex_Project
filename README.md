# Pokedex_Project

I wish to create a GUI to display pokemon data, using Python (Kivy) and JSON file to store data.
I have already made a script that can reach some website to get data and append it to a JSON file.


Next steps:
  - Work to make a new script that can download images and store them in a file, to finally add the path to the DB (JSON).
  - Optimize my current code and implement function.
  - Make a GUI with Kivy. The GUI will display data using this shema:
  
  
                - Main screen:
                          - Display a full list of pokemon ( Mini Image, ID, NAME english, TYPE).
                          - Sorting option (sort by name, by type, by id...), return a new list of pokemon instead of the full list.
                          - If you click on one item from the list it will display a new screen.
                - Second Screen:
                          - Diplay more informations about the choosen pokemon from the main screen
                            ID, Base stat, Images (Normal, Shiny, Gif...), Names (French, Deutsch, Japanese and Korean), Type with images,
                            Abilities with info, list of moves by level up and tm.
                          - A button to go back to main screen
                      
                
