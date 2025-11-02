"""
AWS Documentation Scraper for Customer Service AI

This script helps automate the collection of AWS Lambda and API Gateway documentation.
It downloads documentation pages and converts them to clean markdown format.

Usage:
    python scrape_aws_docs.py --category technical
    python scrape_aws_docs.py --category configuration
    python scrape_aws_docs.py --category billing
    python scrape_aws_docs.py --all

Requirements:
    pip install requests beautifulsoup4 markdownify
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import json

try:
    import requests
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4 markdownify")
    sys.exit(1)

# AWS Documentation URLs organized by category
AWS_DOCS_URLS = {
    "technical": [
        {
            "url": "https://docs.aws.amazon.com/lambda/latest/dg/lambda-troubleshooting.html",
            "title": "lambda-troubleshooting",
            "subcategory": "error_handling"
        },
        {
            "url": "https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html",
            "title": "cloudwatch-debugging-guide",
            "subcategory": "monitoring"
        },
        {
            "url": "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-error-codes.html",
            "title": "api-gateway-error-codes",
            "subcategory": "error_handling"
        },
        {
            "url": "https://docs.aws.amazon.com/lambda/latest/dg/foundation-arch.html",
            "title": "cold-start-optimization",
            "subcategory": "performance"
        },
        {
            "url": "https://docs.aws.amazon.com/lambda/latest/dg/troubleshooting-vpc.html",
            "title": "lambda-vpc-connectivity",
            "subcategory": "integration"
        },
    ],
    "configuration": [
        {
            "url": "https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html",
            "title": "lambda-best-practices",
            "subcategory": "best_practices"
        },
        {
            "url": "https://docs.aws.amazon.com/lambda/latest/dg/lambda-security.html",
            "title": "lambda-security-guidelines",
            "subcategory": "security"
        },
        {
            "url": "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html",
            "title": "lambda-authorizers-guide",
            "subcategory": "security"
        },
        {
            "url": "https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html",
            "title": "cors-configuration",
            "subcategory": "networking"
        },
        {
            "url": "https://docs.aws.amazon.com/lambda/latest/operatorguide/design-patterns.html",
            "title": "serverless-architecture-patterns",
            "subcategory": "architecture"
        },
    ],
    "billing": [
        {
            "url": "https://aws.amazon.com/lambda/pricing/",
            "title": "lambda-pricing-details",
            "subcategory": "pricing"
        },
        {
            "url": "https://aws.amazon.com/api-gateway/pricing/",
            "title": "api-gateway-pricing-comparison",
            "subcategory": "pricing"
        },
    ]
}

class AWSDocScraper:
    def __init__(self, output_dir: str = "../data"):
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_page(self, url: str) -> tuple:
        """Scrape a single AWS documentation page and return content and title."""
        try:
            print(f"  Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find the main content area (AWS docs structure)
            main_content = soup.find('div', {'id': 'main-col-body'})
            if not main_content:
                main_content = soup.find('main')
            if not main_content:
                main_content = soup.find('div', {'class': 'awsui-util-container'})
            
            if not main_content:
                print(f"  WARNING: Could not find main content area")
                return None, None
            
            # Get title
            title_elem = soup.find('h1')
            title = title_elem.get_text().strip() if title_elem else "AWS Documentation"
            
            # Remove navigation, footer, and other non-content elements
            for element in main_content.find_all(['nav', 'footer', 'script', 'style']):
                element.decompose()
            
            # Convert to markdown
            markdown_content = md(str(main_content))
            
            return markdown_content, title
            
        except requests.exceptions.RequestException as e:
            print(f"  ERROR: Failed to fetch {url}: {e}")
            return None, None
        except Exception as e:
            print(f"  ERROR: Failed to process {url}: {e}")
            return None, None
    
    def create_metadata_header(self, category: str, subcategory: str, url: str, service: str = "lambda") -> str:
        """Create metadata header for markdown file."""
        return f"""---
category: {category}
subcategory: {subcategory}
service: {service}
difficulty: intermediate
last_updated: {datetime.now().strftime('%Y-%m-%d')}
source: {url}
---

"""
    
    def save_document(self, content: str, filename: str, category: str, metadata: str):
        """Save document to appropriate directory."""
        category_dir = self.output_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = category_dir / f"{filename}.md"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(metadata)
            f.write(content)
        
        print(f"  ✓ Saved: {filepath}")
        return filepath
    
    def scrape_category(self, category: str):
        """Scrape all documents for a given category."""
        if category not in AWS_DOCS_URLS:
            print(f"ERROR: Unknown category '{category}'")
            return
        
        print(f"\n{'='*60}")
        print(f"Scraping {category.upper()} documentation...")
        print(f"{'='*60}\n")
        
        docs = AWS_DOCS_URLS[category]
        success_count = 0
        
        for doc_info in docs:
            url = doc_info["url"]
            title = doc_info["title"]
            subcategory = doc_info["subcategory"]
            
            # Determine service from URL
            if "apigateway" in url:
                service = "api-gateway"
            elif "lambda" in url:
                service = "lambda"
            else:
                service = "aws"
            
            print(f"\n📄 Processing: {title}")
            content, page_title = self.scrape_page(url)
            
            if content:
                metadata = self.create_metadata_header(category, subcategory, url, service)
                
                # Add page title as H1 if not already present
                if page_title and not content.strip().startswith('#'):
                    content = f"# {page_title}\n\n{content}"
                
                self.save_document(content, title, category, metadata)
                success_count += 1
            else:
                print(f"  ✗ Failed to scrape: {title}")
        
        print(f"\n{'='*60}")
        print(f"✓ Completed {category}: {success_count}/{len(docs)} documents scraped")
        print(f"{'='*60}\n")
    
    def scrape_all(self):
        """Scrape all categories."""
        for category in AWS_DOCS_URLS.keys():
            self.scrape_category(category)
            print("\n")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape AWS documentation for Customer Service AI"
    )
    parser.add_argument(
        '--category',
        choices=['technical', 'configuration', 'billing'],
        help='Specific category to scrape'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Scrape all categories'
    )
    parser.add_argument(
        '--output',
        default='../data',
        help='Output directory (default: ../data)'
    )
    
    args = parser.parse_args()
    
    if not args.category and not args.all:
        parser.error("Please specify --category or --all")
    
    scraper = AWSDocScraper(output_dir=args.output)
    
    if args.all:
        scraper.scrape_all()
    else:
        scraper.scrape_category(args.category)
    
    print("\n✅ Scraping complete!")
    print("\nNext steps:")
    print("1. Review the generated markdown files")
    print("2. Clean up any formatting issues")
    print("3. Add additional manual documentation as needed")
    print("4. Proceed to Stage 2: Data Ingestion Pipeline")


if __name__ == "__main__":
    main()

