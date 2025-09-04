import pandas as pd
from pathlib import Path
import sys

class LivingLibrary:
    def __init__(self, spreadsheet_path):
        self.df = self.load_library_data(spreadsheet_path)
        
    def load_library_data(self, file_path):
        try:
            file_path = Path(file_path)
            if file_path.suffix == '.xlsx':
                df = pd.read_excel(file_path)
            elif file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            else:
                raise ValueError("Unsupported file format. Use .xlsx or .csv")
            # ID for reference
            df['ID'] = range(1, len(df) + 1)

            # Convert Year column to string, handling NaN values
            df['Year'] = df['Year'].fillna('Unknown').astype(str).str.replace('.0', '', regex=False)
            
            # Combine authors into a single column
            author_cols = ['Author 1', 'Author 2', 'Author 3', 'Author 4', 'Author 5']
            df['Authors'] = df[author_cols].fillna('').apply(
                lambda x: ', '.join([str(val) for val in x if val != '' and str(val) != 'n/a']), axis=1
            )
            df['Authors'] = df['Authors'].replace('', 'Unknown')
            
            return df
        except Exception as e:
            print(f"Error loading file: {e}")
            return pd.DataFrame()
        

    def display_inventory(self, filter_type=None):
        display_df = self.df.copy()
        
        if filter_type:
            display_df = display_df[display_df['Type'].str.contains(filter_type, case=False, na=False)]
        
        if display_df.empty:
            print("Inventory is empty.")
            return
            
        print("\n" + "="*50)
        print("MY LIVING LIBRARY.")
        print("="*50)

        for _, row in display_df.iterrows():
            print(f"{row['ID']:3d}. {row['Title']}")
            print(f"     Authors: {row['Authors']}")
            print(f"     Type: {row['Type']} | Format: {row['Format']}")
            print(f"     Topic: {row['Topic']}")
            print(f"     Publisher: {row['Publisher']} ({row['Year']})")
            if 'Free Download' in row and str(row['Free Download']).lower() in ['yes']:
                print(" You can download this for free!")
            print("-" * 50)
    
    def search_books(self, query):
        # Search by title, author, or topic
        query = query.lower()
        matches = self.df[
            self.df['Title'].str.contains(query, case=False, na=False) |
            self.df['Authors'].str.contains(query, case=False, na=False) |
            self.df['Topic'].str.contains(query, case=False, na=False) |
            self.df['Subtitle'].str.contains(query, case=False, na=False)
        ]
        
        if matches.empty:
            print(f"No items found matching '{query}'")
            return
            
        print(f"\nSearch results for '{query}':")
        print("-" * 50)
        for _, row in matches.iterrows():
            authors_short = row['Authors'][:50] + "..." if len(str(row['Authors'])) > 50 else row['Authors']
            print(f"{row['ID']:3d}. {row['Title']}")
            print(f"     By: {authors_short} | Topic: {row['Topic']}")
            print(f"     Type: {row['Type']} | Format: {row['Format']}")
            print("-" * 50)
    
    def access_item(self, book_id):
        """view an item by ID"""
        try:
            book_id = int(book_id)
            if book_id not in self.df['ID'].values:
                return -1, "Invalid item ID"
            
            book_idx = self.df[self.df['ID'] == book_id].index[0]
            item = self.df.iloc[book_idx]
            
            # Show item details
            print(f"\nAccessing: {item['Title']}")
            print(f"Authors: {item['Authors']}")
            print(f"Type: {item['Type']} | Format: {item['Format']}")
            print(f"Topic: {item['Topic']}")
            print(f"Publisher: {item['Publisher']} ({item['Year']})")
            
            if pd.notna(item['Subtitle']):
                print(f"Subtitle: {item['Subtitle']}")
            
            # Check if it's a free download
            if 'Free Download' in self.df.columns and str(item['Free Download']).lower() in ['yes', 'true']:
                print(" This item is available as a free download!")

            return 0, "Item details displayed"

        except ValueError:
            return -1, "Please enter a valid item ID number"
    
    def get_types(self):
        """Get all unique types in the library"""
        return self.df['Type'].unique()

def check_quit_or_back(user_input):
    """Check if user wants to quit or go back"""
    quit_words = ["!q", "quit", "exit"]
    back_words = ["!b", "back", "return", "menu"]
    
    user_input = user_input.lower().strip()
    
    if user_input in quit_words:
        print("Thank you for visiting the Living Library. Goodbye!")
        return "QUIT"
    elif user_input in back_words:
        return "BACK"  
    return False

def safe_input(prompt):
    """Input function that checks for quit/back commands"""
    user_input = input(prompt)
    
    if check_quit_or_back(user_input):
        return "BACK" 
    
    return user_input


def main():
    spreadsheet_path = "data\justLib.csv"
    if not Path(spreadsheet_path).exists():
        print(f"Spreadsheet not found at {spreadsheet_path}")
        print("Please update the spreadsheet_path variable with the correct file path.")
        return
    
    library = LivingLibrary(spreadsheet_path)
    
    if library.df.empty:
        print("DataFrame appears to be empty. Exiting.")
        return
    
    # Command shortcuts
    quit_words = ["!q", "quit", "exit"]
    back_words = ["!b", "back", "return", "menu"]
    access_words = ["a", "access", "view", "open"]
    inventory_words = ["i", "inventory", "list", "show", "browse"]
    search_words = ["s", "search", "find"]
    
    while True:
        print("\n" + "="*50)
        print("Welcome to the Living Library.")
        print("="*50 + "\n")
        print(f"Loaded {len(library.df)} items from the library, lets find you the perfect resource...")
        print() # I will consider using f-strings for this or tabulate later
        print("Available Commands: ")
        print(  
            "  a/access    - View item details \n" \
            "  i/inventory - Show inventory \n" \
            "  s/search    - Search catalog\n")
        print("Life Hacks: ")
        print(  
            "  !b/back      - Back to main menu\n" \
            "  !q/quit      - Exit")
        user_choice = safe_input("\nEnter Command: ").lower().strip()

        # Check if user wants to go back (from safe_input)
        if user_choice == "BACK":
            continue

        if user_choice in quit_words:
            print("Thank you for visiting the Living Library. Goodbye!")
            break
            
        elif user_choice in access_words:
            library.display_inventory()
            book_id = safe_input("\nEnter item ID to view details: ")
            
            if book_id == "QUIT":
                print("Thank you for visiting the Living Library. Goodbye!")
                return
            elif book_id == "BACK":
                continue
                
            result, message = library.access_item(book_id)
            if result == 0:
                print(message)
            else:
                print(f"Error: {message}")
            
        elif user_choice in inventory_words:
            types = library.get_types()
            print(f"\nAvailable types: {', '.join(types)}")
            topics = library.df['Topic'].unique()
            print(f"\nAvailable topics: {', '.join(topics[:3])}..." if len(topics) > 10 else f"Available topics: {', '.join(topics)}")
            filter_choice = safe_input("\nFilter by type or topic (or press Enter for all): ").strip()
            
            if filter_choice == "QUIT":
                print("Thank you for visiting the Living Library. Goodbye!")
                return
            elif filter_choice == "BACK":
                continue
                
            library.display_inventory(filter_choice if filter_choice else None)

            pause = safe_input("\nPress Enter to return to main menu...")
            if pause == "QUIT":
                print("Thank you for visiting the Living Library. Goodbye!")
                return
    # Continue to main menu            
        elif user_choice in search_words:
            while True: 
                topics = library.df['Topic'].unique()
                print("\n" + "="*50)
                print("Available Topics:")
                print(f"Available topics: {', '.join(topics[:10])}..." if len(topics) > 10 else f"Available topics: {', '.join(topics)}")
                print("="*50)
                
                query = safe_input("Enter search term (title, author, or topic): ")

                if query in ["QUIT", "BACK"]:
                    break

                library.search_books(query)

                found = safe_input("Did you find what you were looking for? (yes/no): ").lower()
                if found in ['yes', 'y']:
                    # Assuming a link column exists in the CSV
                    # For now, let's just ask for an ID and access it
                    link_id = safe_input("Enter the ID of the item you want to access: ")
                    if link_id in ["QUIT", "BACK"]:
                        break
                    library.access_item(link_id)
                    print("Thank you for visiting the Living Library. Goodbye!")
                    return # Exit the entire program

                elif found in ['no', 'n']:
                    continue  # Go back to the search prompt

                else:
                    print("Invalid input. Returning to main menu.")
                    break

        else:
            print("Invalid command. Please try again.")
            continue

if __name__ == "__main__":
    main()