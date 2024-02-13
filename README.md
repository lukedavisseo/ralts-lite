# RALTS Lite (Really Awesome Lexicon and Tag Suggester)

**A Streamlit web app that performs NLP analysis on a body of text or URL.**

Image coming soon!

# Table of Contents
 - [What is RALTS Lite?](#what-is-ralts)
 - [What is RALTS Lite for?](#what-is-ralts-for)
 - [Example use cases](#example-use-cases)
 - [Installation](#installation)
 - [Example Experiments](#example-experiments)
 - [Share with Others](#share-with-others)
 - [Features](#features) (see the [docs](https://chainforge.ai/docs/nodes/) for more comprehensive info)
 - [Development and How to Cite](#development)

## What is RALTS Lite?

RALTS Lite (Really Awesome Lexicon and Tag Suggester) is a Streamlit web app that performs NLP analysis on a body of text or URL. It uses two APIs to perform these tasks:

1. The TextRazor API, which extracts entities, topics, and categories from any given text
2. The Hugging Face Inference API, which accesses a language model to figure out what that body of text is about, based on the extract topics

RALTS Lite is smaller version of RALTS Lite, an app I built for myself. If you want a lengthy explanation of why I built that app, [you can read about it on my website](https://lukealexdavis.co.uk/posts/introducing-ralts/)

## What is RALTS Lite for?

RALTS Lite is geared towards SEOs who want to know what a body of text is about, which can help with a variety of tasks such as:

 - General optimisation - rather than focus solely on keywords, finding entities and topics can help with topical relevance
 - Keyword research - extracting various entities and topics from a website can show where there are common themes or content gaps 
 - Internal linking - finding commonality between pages could unearth linking opportunities

Please note: this is an internal tool which has API keys stored within the backend. Please don't share this with anyone outside of the business.

# Example use cases

Say you're wanting to optimise [a blog post about page speed](https://www.impressiondigital.com/blog/page-speed/). A way you could do this is to identify what the page is about and improve its relevance for certain topics or include topics that are missing.

More on this section coming soon...

----------------------------------

# Development

RALTS Lite was created by me.

## Inspiration

RALTS Lite was inspired by [IBM's Watson API demo](https://www.ibm.com/demos/live/natural-language-understanding/self-service/home) but elaborates on their work further, via a free API. The ultimate goal is offer an additional point of analysis in our optimisation work. As Google has moved away from keywords and towards topics, it's important to understand what topics arise from content, especially when tools like Ahrefs and Semrush tend to focus more on keywords.

# License

RALTS Lite is released under the MIT License.
