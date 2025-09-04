import pandas as pd
from pathlib import Path

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
        print("MY LIVING LIBRARY, \nWelcome to the Dojo.")
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
            
            return 0, f"Item details displayed"
            
        except ValueError:
            return -1, "Please enter a valid item ID number"
    
    def get_types(self):
        """Get all unique types in the library"""
        return self.df['Type'].unique()

def main():
    # Initialize library - UPDATE THIS PATH TO YOUR SPREADSHEET
    spreadsheet_path = "data\justLib.csv"  # Change this to your file path
    
    if not Path(spreadsheet_path).exists():
        print(f"Spreadsheet not found at {spreadsheet_path}")
        print("Please update the spreadsheet_path variable with the correct file path.")
        return
    
    library = LivingLibrary(spreadsheet_path)
    
    if library.df.empty:
        print("Failed to load library data. Exiting.")
        return
    

    
    # Command shortcuts
    quit_words = ["q", "quit", "exit"]
    access_words = ["a", "access", "view", "open"]
    inventory_words = ["i", "inventory", "list", "show", "browse"]
    search_words = ["s", "search", "find"]
    
    while True:
        print("\n" + "="*50)
        print("Welcome to the Living Library.")
        print("="*50 + "\n")
        print(f"Loaded {len(library.df)} items from the library, lets find you the perfect resource...")
        print()
        print("Available Commands: ")
        print(  
            "  a/access    - View item details \n" \
            "  b/browse    - Browse all items\n" \
            "  i/inventory - Show inventory (filter by type)\n" \
            "  s/search    - Search catalog\n" \
            "  q/quit      - Exit")
        user_choice = input("\nEnter Command: ").lower().strip()

        if user_choice in quit_words:
            return "Thank you for visting the Living Library. Goodbye!"
            
        elif user_choice in access_words:
            library.display_inventory()
            book_id = input("\nEnter item ID to view details: ")
            message = library.access_item(book_id)
            print(message)
            
        elif user_choice in inventory_words:
            types = library.get_types()
            print(f"\nAvailable types: {', '.join(types)}")
            topics = library.df['Topic'].unique()
            print(f"\nAvailable topics: {', '.join(topics[:10])}..." if len(topics) > 10 else f"Available topics: {', '.join(topics)}")
            filter_choice = input("Filter by type or topic (or press Enter for all): ").strip()
            library.display_inventory(filter_choice if filter_choice else None)
            
        elif user_choice in search_words:
            query = input("Enter search term (title, author, or topic): ")
            library.search_books(query)
            
        else:
            print("Invalid command. Please try again.")
            continue

if __name__ == "__main__":
    main()