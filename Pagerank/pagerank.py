import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    total_pages = len(corpus) #calculate the total number of pages in corpus
    linked_pages = corpus[page] #get the set of pages liked to this corpus page 
    if not linked_pages: #if this corpus page doesn't have any pages 
        linked_pages = set(corpus.keys()) #then set 'linked_pages to include all the pages in corpus

    probability = (1 - damping_factor) / total_pages #probability of choosing any page from the corpus 
    damping_probability = damping_factor / len(linked_pages) #Calculate the probability of choosing any linked page from the current page with equal probability 

    model = {page: probability for page in corpus } #initialize a dictionary 

    for linked_page in linked_pages:
        model[linked_page] += damping_probability

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    total_pages = len(pages)
    sample_count = n

    # Initialize the count for each page to 0
    page_counts = {page: 0 for page in pages}

    # Choose a random starting page
    current_page = random.choice(pages)

    for _ in range(n):
        # Update the count for the current page in the sample
        page_counts[current_page] += 1

        # Generate a transition model for the current page
        model = transition_model(corpus, current_page, damping_factor)

        # Choose the next page based on the transition model
        next_page = random.choices(pages, weights=list(model.values()))[0]

        # Move to the next page for the next iteration
        current_page = next_page

    # Convert counts to proportions (PageRank values)
    pagerank = {page: count / sample_count for page, count in page_counts.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    initial_rank = 1 / total_pages

    # Initialize the PageRank dictionary with initial ranks
    pagerank = {page: initial_rank for page in corpus}

    # Helper function to calculate the sum of PageRanks for pages that link to a given page
    def calculate_link_sum(page):
        return sum(pagerank[link] / len(corpus[link]) for link in corpus if page in corpus[link])

    # Loop until convergence (change in PageRank is less than 0.001)
    while True:
        new_pagerank = {}

        for page in corpus:
            new_pagerank[page] = (1 - damping_factor) / total_pages + damping_factor * calculate_link_sum(page)

        # Calculate the maximum change in PageRank value
        max_change = max(abs(new_pagerank[page] - pagerank[page]) for page in corpus)

        # Break the loop if the maximum change is less than 0.001
        if max_change < 0.001:
            break

        pagerank = new_pagerank

    return pagerank


if __name__ == "__main__":
    main()
