import subprocess
import pandas as pd
# Define the Scrapy command

def find_and_replace(file_path, old_text, new_text):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        file_data = file.read()

    # Replace the target string
    file_data = file_data.replace(old_text, new_text)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(file_data)

    print(f"Replaced all occurrences of '{old_text}' with '{new_text}' in '{file_path}'.")

# Example usage

file_path = r'C:\college\web mining project\crawler\nueralcrawling\nueralcrawling\spiders\crawlig_spider.py'

df =  pd.read_csv(r'C:\college\web mining project\crawler2\crawler2\tourism_links.csv')
df = df.iloc[18:,:].reset_index().iloc[:,1:]

previous_rule = 'test'
previous_url = 'test'
for i in range(df.shape[0]):

    #for change in rule
    current_rule = df.loc[i, 'rule']
    old_text = f"Rule(LinkExtractor(allow='{previous_rule}')"
    new_text = f"Rule(LinkExtractor(allow='{current_rule}')"
    find_and_replace(file_path, old_text, new_text)
    previous_rule = current_rule

    # for change in url
    current_url = df.loc[i, 'url']
    old_text = f"start_urls = ['{previous_url}']"
    new_text = f"start_urls = ['{current_url}']"
    find_and_replace(file_path, old_text, new_text)
    previous_url = current_url



    command = f"scrapy crawl myspider -o {df.loc[i,'name']}.csv"

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(e)

# Run the command

