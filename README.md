# LoLify

LoLify is a web-app that uses RiotGames API for the game League of Legends. The web-app sorts through a player's match history and displays their stats, and allows them to create a user profile for other feedback.

#### App Features Include:
* The ability to create an account, allowing the user to:
    * Pin their favorite League Of Legends account or their own personal account.
    * Edit and update their account to display a different users stats.
    

    
* User can search any active league of legends user and view their match history:
    * This will display in-game stats
    * It will show which team won/lost

## Installation

To run LoLify on your local machine, follow these steps:

1. Use python3.7 to create a virtual environment: python3.7 -m venv myenv
2. Activate the virtual environment: source myenv/bin/activate
3. Clone this repository to your local machine: git clone https://github.com/[username]/LoLify.git
4. Navigate to the project directory: cd LoLify
5. Install the requirements.txt file using pip3: pip3 install -r requirements.txt
6. Create a .env file and add your RiotGames API key: RIOT_API_KEY=[your api key]
7. Run the Flask server: flask run
8. Navigate to http://localhost:5000 in your web browser

## Usage

1. Enter a League of Legends summoner name
2. View player stats and match history
3. Create a user profile for feedback

## Technologies Used

- Flask
- Python
- HTML
- CSS
- RiotGames API - Library LolWatcher

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/) - see the LICENSE file for details.
