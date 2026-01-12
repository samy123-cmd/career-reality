import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

def count_words(text):
    if not text:
        return 0
    return len(text.split())

def analyze_content():
    articles = Article.objects.all()
    thin_count = 0
    total_articles = 0
    
    with open('audit_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"{'ID':<4} | {'Word Count':<10} | {'Status':<10} | {'Title'}\n")
        f.write("-" * 100 + "\n")
        
        for article in articles:
            # Combine all substantial fields
            parts = [
                article.common_expectation,
                article.actual_reality,
                article.salary_reality,
                article.stuck_point,
                article.verdict,
                article.target_persona,
                article.who_should_avoid
            ]
            
            # basic cleaning of none
            parts = [p if p else "" for p in parts]
            full_text = " ".join(parts)
            
            word_count = count_words(full_text)
            
            status = "OK"
            if word_count < 600:
                status = "CRITICAL"
                thin_count += 1
            elif word_count < 1000:
                status = "THIN"
                thin_count += 1
                
            try:
                title = article.title[:50] if article.title else "NO TITLE"
                f.write(f"{article.id:<4} | {word_count:<10} | {status:<10} | {title}\n")
            except Exception as e:
                f.write(f"Error printing article {article.id}: {e}\n")
                
            total_articles += 1

        f.write("-" * 100 + "\n")
        f.write(f"Total Articles: {total_articles}\n")
        f.write(f"Thin Content (< 1000 words): {thin_count}\n")
    
    print("Report written to audit_report.txt")

if __name__ == "__main__":
    analyze_content()
