import os
import csv
import random
from datetime import datetime, timedelta

# Create dataset directory if it doesn't exist
os.makedirs("dataset", exist_ok=True)

# Word lists to generate realistic mock news text
subjects_true = ["politicsNews", "worldnews"]
subjects_fake = ["Government News", "Middle-east", "US_News", "left-news", "politics", "left-news"]

true_political_topics = [
    ("Senate Passes Infrastructure Bill with Bipartisan Support", "The Senate passed a major infrastructure funding bill today in a rare display of bipartisan cooperation. The legislation allocates $1.2 trillion for roads, bridges, and broadband expansion. Senators from both sides of the aisle praised the agreement as a necessary step for modernization. Critics raised concerns about the national debt increase, but the bill secured the 60 votes required to pass."),
    ("Prime Minister Announces New Renewable Energy Goals", "The Prime Minister delivered a speech detailing a strategy to transition 80% of national energy output to renewable sources by 2035. The plan includes tax incentives for solar and wind farms, along with subsidies for low-income households. Conservative opposition groups expressed concerns about energy security and grid reliability during transition periods, while environmental organizations hailed the target as ambitious but achievable."),
    ("Federal Reserve Signals Interest Rate Hike to Counter Inflation", "The Federal Reserve indicated it may raise interest rates sooner than anticipated to control rising inflation. Following a meeting of the Federal Open Market Committee, officials noted that consumer demand remains strong, but supply chain issues continue to drive prices upward. Economists project a quarter-percentage-point increase in the benchmark rate by next quarter."),
    ("Supreme Court Rules on Landmark Environmental Regulation Case", "In a 6-3 decision, the Supreme Court ruled on the scope of federal authority to regulate industrial emissions under the Clean Air Act. The majority opinion states that major regulatory actions require explicit congressional authorization. The dissenting justices argued the ruling severely limits the agency's capacity to address climate change effectively."),
    ("Trade Delegation Concludes Talks with Major European Partners", "Trade representatives finished a three-day summit in Brussels, reaching preliminary agreements on tariff reductions for agricultural imports and shared cybersecurity standards. The joint statement emphasized cooperative regulation of artificial intelligence and digital services. A formal treaty is expected to be signed late next month."),
    ("Bipartisan Committee Reports on Cyber Defense Vulnerabilities", "A congressional committee released a report outlining key security vulnerabilities in the nation's energy grids and municipal water networks. The document recommends immediate investments in defense software and mandatory report guidelines for critical infrastructure operators. Both co-chairs emphasized that cyber threats from foreign actors are at an all-time high.")
]

true_world_topics = [
    ("Peace Talks Resume in Geneva Amid High Skepticism", "Diplomats from conflicting regions gathered in Geneva to negotiate a ceasefire. Mediators from the UN stated that while baseline trust is low, both sides have agreed to discuss humanitarian corridors and prisoner exchanges. Observers warn that previous agreements have repeatedly collapsed, urging cautious expectations."),
    ("Global Health Organization Declares Vaccine Distribution Plan", "The Global Health Organization launched an initiative targeting the distribution of 500 million vaccines to developing nations. Funded by a coalition of international donors, the initiative aims to address distribution gaps. Logistical experts noted that cold-chain storage requirements will pose a significant challenge in remote areas."),
    ("International Space Station Crew Successfully Returns to Earth", "A capsule carrying three astronauts splashed down safely in the Pacific Ocean after a six-month research mission aboard the International Space Station. The crew conducted experiments on cellular growth in microgravity and tested new water reclamation systems. NASA confirmed all crew members are in good health and undergoing routine post-flight evaluation."),
    ("Major Infrastructure Project Completed in East Asia", "Engineers celebrated the completion of a high-speed rail line connecting major manufacturing hubs in East Asia. The project, which took seven years and cost billions, is expected to reduce travel times by 60% and lower transport emissions. Local officials hope it will stimulate regional economic development."),
    ("Foreign Ministers Sign Historic Maritime Border Treaty", "Two neighboring countries resolved a decades-old maritime dispute by signing a border treaty. The agreement establishes clear exclusive economic zones and permits shared exploration of offshore natural gas reserves. The resolution is seen as a victory for bilateral diplomacy in the region.")
]

fake_topics = [
    ("BREAKING: Leaked Documents Confirm Alien Base Under the Pentagon!", "Inside sources have leaked highly classified documents proving that a secret alien research facility has operated directly beneath the Pentagon since 1957. The files, which government officials refuse to acknowledge, describe advanced extraterrestrial technology used to control global communication satellites. Share this before it gets taken down!"),
    ("Unbelievable: Local Vegetable Cures Cancer in 24 Hours, FDA BANS It!", "An independent researcher has discovered that a common backyard weed contains enzymes that completely cure cancer in 24 hours. However, instead of making this public, the FDA has classified the study and banned all sales of the plant to protect big pharma profits. The public has a right to know the truth!"),
    ("SHOCKING: Politicians Secretly Planning to Replace Cash with Microchips next Month!", "A whistleblower has revealed that a secret meeting was held last week where top politicians and international bankers finalized a plan to completely outlaw physical cash by next month. Citizens will be forced to accept implanted microchips to buy groceries, allowing the government to track every single purchase and freeze accounts instantly."),
    ("ALERT: Weather Control Machine Discovered in Secret Mountain Bunker", "A hiker stumbled upon an enormous satellite array and underground complex in the Rocky Mountains. Expert analysis suggests this is the notorious weather modification weapon used by shadow agencies to trigger artificial storms and manipulate crop prices. The mainstream media is silent on this massive threat!"),
    ("BOMBSHELL: Proof that NASA Simulated the Entire Solar System in a Hollywood Studio", "A former contractor has released high-definition video footage showing production sets where Mars and Jupiter missions were filmed using green screens. The contractor claims that space exploration is a massive hoax designed to siphon trillions of taxpayer dollars into private space ventures."),
    ("Must Read: Secret Group in Control of the Global Weather Grid Exposed!", "A new leaked report confirms that a secretive global elite has been actively manipulating the jet stream to cause droughts and severe winter weather across selected nations. The report details how microwave transmitters and aerial chemicals are deployed daily. Mainstream news outlets are forbidden from reporting this."),
    ("REVEALED: The Truth About the Secret Government Project in the Desert", "For years, travelers have reported strange lights and humming sounds near the high-security military zone in Nevada. Now, a retired engineer has confirmed that scientists are testing teleportation devices retrieved from ancient archaeological sites. The government is keeping these energy breakthroughs hidden from the public.")
]

subjects_pool_true = ["politicsNews", "worldnews"]
subjects_pool_fake = ["Government News", "Middle-east", "US_News", "left-news", "politics"]

def write_csv(filepath, data):
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["title", "text", "subject", "date"])
        # Write data rows
        writer.writerows(data)

def generate_news_dataset(num_samples=1000):
    true_data = []
    fake_data = []
    
    start_date = datetime.now() - timedelta(days=730) # Over 2 years
    
    # Generate True News
    for i in range(num_samples // 2):
        topic_pool = true_political_topics if random.random() < 0.6 else true_world_topics
        title_base, text_base = random.choice(topic_pool)
        
        variant = random.randint(100, 999)
        subject = random.choice(subjects_pool_true)
        title = f"{title_base} (Update {variant})"
        
        text = text_base + f" The local regional representative stated that over {random.randint(10, 95)}% of surveyed citizens support this measure, according to a recent census update in sector {variant}."
        
        rand_date = start_date + timedelta(days=random.randint(0, 700))
        date_str = rand_date.strftime("%B %d, %Y") + " "
        
        true_data.append([title, text, subject, date_str])
        
    # Generate Fake News
    for i in range(num_samples // 2):
        title_base, text_base = random.choice(fake_topics)
        
        variant = random.randint(100, 999)
        subject = random.choice(subjects_pool_fake)
        title = f"{title_base}!!! (Secret Code: {variant})"
        
        text = text_base + f" Whistleblowers warning code {variant} have urged citizens to wake up and share this viral report immediately before the servers are shut down forever by the deep state operatives."
        
        rand_date = start_date + timedelta(days=random.randint(0, 700))
        date_str = rand_date.strftime("%B %d, %Y")
        
        fake_data.append([title, text, subject, date_str])
        
    write_csv("dataset/True.csv", true_data)
    write_csv("dataset/Fake.csv", fake_data)
    print(f"Generated synthetic dataset: dataset/True.csv ({len(true_data)} rows) and dataset/Fake.csv ({len(fake_data)} rows).")

if __name__ == "__main__":
    generate_news_dataset(1000)
