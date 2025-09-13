APIs for Automated Research Assistant

This report summarises major literature‑retrieval APIs that could be used to build an automatic research assistant. For each API we describe endpoints, input parameters, typical responses, authentication requirements and rate limits. Citations come from the latest official documentation or reputable summaries.

1. arXiv API
Purpose

The arXiv API provides programmatic access to preprint metadata (titles, abstracts, authors, etc.). It is free to use and does not require authentication, but you should follow polite usage guidelines.

Search API

Base URL: http://export.arxiv.org/api/query.

Parameters:

search_query – Lucene‑like string used to search metadata. Prefixes (e.g., ti: for title, au: for author) may be combined with Boolean operators. If search_query is present and id_list is not, the API returns all matching papers
info.arxiv.org
.

id_list – comma‑separated list of arXiv identifiers. If only id_list is given, the API returns those identifiers; if both parameters are present, results are filtered by the query
info.arxiv.org
.

start and max_results – integers for pagination. start defines the zero‑based index of the first result; max_results limits returned results (default 10). The API recommends using slices of ≤2,000 and limits a single call to ≤30,000 results
info.arxiv.org
.

sortBy and sortOrder – optional. sortBy can be relevance, lastUpdatedDate or submittedDate, and sortOrder can be ascending or descending
info.arxiv.org
.

Response: Atom feed (XML) containing metadata. Each <entry> element holds a paper’s title, authors, abstract, categories and other fields
info.arxiv.org
.

Rate limits: None specified, but arXiv requests that scripts pause ~3 s between requests and avoid very large queries to reduce server load
info.arxiv.org
.

Submission API

The arXiv submission API (separate from search) uses OAuth2. Clients request access tokens via a client_credentials grant and pass the token in an Authorization: Bearer header to submit manuscripts. This API is not needed for a research assistant unless it will submit articles on behalf of users.

3. Semantic Scholar API

Semantic Scholar offers REST APIs organised in three categories: Academic Graph, Recommendations and Datasets. Most endpoints are public and do not require a key, but personal API keys can be requested for higher reliability.

Base URLs and Authentication

Academic Graph API: https://api.semanticscholar.org/graph/v1 – provides paper, author, citation, reference and venue data
semanticscholar.org
.

Recommendations API: https://api.semanticscholar.org/recommendations/v1 – recommends papers based on other papers
semanticscholar.org
.

Datasets API: https://api.semanticscholar.org/datasets/v1 – download large snapshot datasets
semanticscholar.org
.

Authentication: No API key required, but using one is recommended. Without a key, users share a global anonymous key that permits roughly 1000 requests per second. Personal API keys, passed in the x-api-key header, grant a private limit of about 1 request per second
semanticscholar.org
.

Important Endpoints

Below are commonly used endpoints (all under /graph/v1 unless noted). Each supports the fields query parameter to specify which attributes to return.

Endpoint	Description	Notes
GET /paper/{paper_id}	Returns detailed metadata for a paper (title, abstract, authors, citation count, etc.). paper_id may be a Semantic Scholar ID, DOI, arXiv ID or other identifier.	Use fields to select returned fields (e.g., title,year,abstract,citationCount)
semanticscholar.org
.
GET /paper/{paper_id}/authors	Returns authors of a paper.	Optional limit parameter controls number of results.
GET /paper/{paper_id}/citations	Returns papers that cite the given paper.	Supports pagination.
GET /paper/{paper_id}/references	Returns papers referenced by the given paper.	
GET /paper/search	Searches for papers using the query parameter. Optional filters include year, venue, publication_types, fields_of_study, open_access_pdf, min_citation_count, limit (≤100), sort (e.g., year:desc) and bulk=true for large result sets.	Bulk endpoint returns pages of 1 000 results and up to 10 million results total.
GET /author/{author_id}	Returns details of an author (name, affiliations, etc.).	
GET /author/{author_id}/papers	Returns papers authored by an author.	Optional limit and fields.
Additional Notes

API responses are JSON. The tutorial emphasises that including only needed fields improves performance
semanticscholar.org
.

Example call: https://api.semanticscholar.org/graph/v1/paper/10.1145/3313831.3376727?fields=title,authors returns a paper’s title and author list without requiring a key.

4. OpenAlex API

OpenAlex is an open index of scholarly works, authors, institutions and related entities. The API is free, no key needed, and is designed for high‑volume access.

Overview

Base URL: https://api.openalex.org.

Authentication: None required. The API imposes a generous daily limit of 100 000 requests per user and suggests including a mailto=your_email parameter for best performance
docs.openalex.org
.

Entities: Works (papers), Authors, Institutions, Sources (journals), Topics, Publishers, Funders, etc. Each entity type has endpoints to fetch a single entity, search/filter lists of entities, and group entities.

Key Endpoints

Get a single work: GET /works/{id}. {id} may be an OpenAlex ID (e.g., W2741809807) or an external ID (DOI, PMID, PMCID, MAG). Example: https://api.openalex.org/works/W2741809807 returns a JSON object with fields such as id, doi, title, display_name, publication_year and publication_date
docs.openalex.org
. External IDs may be passed as URNs (e.g., /works/https://doi.org/10.7717/peerj.4375 or /works/pmid:14907713)
docs.openalex.org
.

Lists of works: GET /works with parameters like filter (e.g., from_publication_date:2024-01-01), search (full‑text search), sort, per_page (≤200) and page. Similar endpoints exist for authors (/authors), sources (/sources), etc.

Grouping: GET /works/group_by=field or /authors etc. to aggregate counts.

Rate limits: 100 k requests/day, ~10 requests/second (polite pool). Up to 50 IDs can be requested in one call when retrieving lists
docs.openalex.org
.

5. Crossref REST API (Other Useful API)

Crossref’s REST API provides metadata for journal articles, books, conference proceedings and other items registered with Crossref. It is a helpful complement when arXiv or other sources lack metadata.

Base URL: https://api.crossref.org/.

Authentication: No API key is required; however, Crossref encourages users to include a mailto=your_email query parameter to identify themselves.

Rate limits: Crossref runs two pools – polite and public. The public pool allows about 50 requests per second per IP. Exceeding this results in HTTP 503. A metadata plus plan offers higher limits. Rates may change as Crossref balances load.

Key endpoints:

GET /works – search across all works using parameters like query, filter (e.g., from-pub-date, until-pub-date, has-license:true), rows (number of results, maximum 2000) and offset. Example: https://api.crossref.org/works?query=blood&rows=0 returns the total count of works matching “blood”
crossref.org
.

GET /works/{doi} – retrieve metadata for a specific DOI. Appending .json returns JSON; .xml returns XML
crossref.org
.

GET /types – lists content types; GET /types/{type}/works lists works of a given type
crossref.org
.

GET /members – lists Crossref members; accepts rows and offset parameters. There is a maximum row limit of 2000
crossref.org
.

Response: JSON by default, with top‑level keys status, message-type, message-version and a message object containing metadata.

6. Recommendations and Conclusion

Use multiple sources: For a complete literature review, integrate several APIs. arXiv and Springer Nature cover preprints and published papers; Semantic Scholar and OpenAlex provide comprehensive metadata, citation graphs and additional search capabilities; Crossref fills gaps and provides DOIs and licensing information.

Authentication and rate limits: Only Springer Nature requires an API key. Semantic Scholar offers optional API keys that improve reliability. arXiv, OpenAlex and Crossref do not require keys but have usage guidelines.

Query formulation: Each API has its own query language (Lucene for arXiv, fielded q= for Springer Nature, simple strings with filters for Semantic Scholar and OpenAlex, and query/filter for Crossref). Building a research assistant may require normalising user queries into the appropriate formats.

Output parsing: Responses are typically JSON or XML. The assistant should parse each format and extract titles, abstracts, authors, dates and DOIs. Springer Nature’s JATS XML may require additional parsing.

These APIs provide the foundation for building an automated research assistant that can search current literature, retrieve up‑to‑date metadata and (in some cases) full texts, and generate citations.



# DOAJ:

GET
/api/search/articles/{search_query}
Search articles

Search articles

Parameters
Try it out
Name	Description
search_query *
string
(path)
What you are searching for, e.g. computers

You can search inside any field you see in the results or the schema. More details
For example, to search for all articles with abstracts containing the word "shadow"
bibjson.abstract:"shadow"
Short-hand names are available for some fields
doi:10.3389/fpsyg.2013.00479
issn:1874-9496
license:CC-BY
title:hydrostatic pressure
search_query
page
integer
(query)
Which page of the results you want to see.

page
pageSize
integer
(query)
How many results per page you want to see. The default is 10. The page size limit is 100

pageSize
sort
string
(query)
Substitutions are also available here for convenience
title - order by the normalised, unpunctuated version of the title
For example
title:asc
sort
Responses
Response content type

application/json
Code	Description
200	
Search was successful

Example Value
Model
{
  "page": 0,
  "pageSize": 0,
  "query": "string",
  "results": [
    {
      "bibjson": {
        "abstract": "string",
        "author": [
          {
            "affiliation": "string",
            "email": "string",
            "name": "string",
            "orcid_id": "string"
          }
        ],
        "end_page": "string",
        "identifier": [
          {
            "id": "string",
            "type": "string"
          }
        ],
        "journal": {
          "country": "string",
          "language": [
            "string"
          ],
          "number": "string",
          "publisher": "string",
          "title": "string",
          "volume": "string"
        },
        "keywords": [
          "string"
        ],
        "link": [
          {
            "content_type": "string",
            "type": "string",
            "url": "string"
          }
        ],
        "month": "string",
        "start_page": 0,
        "subject": [
          {
            "code": "string",
            "scheme": "string",
            "term": "string"
          }
        ],
        "title": "string",
        "year": "string"
      },
      "created_date": "string",
      "id": "string",
      "last_updated": "string"
    }
  ],
  "timestamp": "string",
  "total": 0
}
400	
Bad Request


GET
/api/search/journals/{search_query}
Search journals

How-To Guide on Search API
Query string syntax
If you'd like to do more complex queries than simple words or phrases, read https://www.elastic.co/guide/en/elasticsearch/reference/1.4/query-dsl-query-string-query.html#query-string-syntax. The DOAJ database is built on Elasticsearch and knowing more about its query syntax will let you send more advanced queries. (This is not a prerequisite for using the DOAJ API - in the sections below, we provide instructions for the most common use cases.) If you think that what you have achieved with the API would be useful for others to know and would like us to add an example to this documentation, submit it to our API group.

Searching inside a specific field
When you are querying on a specific field you can use the json dot notation used by Elasticsearch, so for example to access the journal title of an article, you could use

bibjson.journal.title:"Journal of Science"
Note that all fields are analysed, which means that the above search does not look for the exact string "Journal of Science". To do that, add ".exact" to any string field (not date or number fields) to match the exact contents:

bibjson.journal.title.exact:"Journal of Science"
Special characters
All forward slash / characters will be automatically escaped for you unless you escape them yourself. This means any forward slashes / will become \/ which ends up encoded as %5C/ in a URL. A"naked" backslash \ is not allowed in a URL. You can search for a DOI by giving the articles endpoint either of the following queries (they will give you the same results):

doi:10.3389/fpsyg.2013.00479
doi:10.3389%5C/fpsyg.2013.00479
Short field names
For convenience we also offer shorter field names for you to use when querying. Note that you cannot use the ".exact" notation mentioned above on these substitutions.

The substitutions for journals are as follows:

title - search within the journal's title
issn - the journal's issn
publisher - the journal's publisher (not exact match)
license - the exact license
In addition, if you have a publisher account with the DOAJ, you may use the field "username" to query for your own publicly available journal records. Usernames are not available in the returned journal records, and no list of usernames is available to the public; you need to know your own username to use this field. You would include "username:myusername" in your search.

The substitutions for articles are as follows:

title - search within the article title
doi - the article's doi
issn - the article's journal's ISSN
publisher - the article's journal's publisher (not exact match)
abstract - search within the article abstract
Sorting of results
Each request can take a "sort" url parameter, which can be of the form of one of:

sort=field
sort=field:direction
The field again uses the dot notation.

If specifying the direction, it must be one of "asc" or "desc". If no direction is supplied then "asc" is used.

So for example

sort=bibjson.title
sort=bibjson.title:desc
Note that for fields which may contain multiple values (i.e. arrays), the sort will use the "smallest" value in that field to sort by (depending on the definition of "smallest" for that field type)

The query string - advanced usage
The format of the query part of the URL is that of an Elasticsearch query string, as documented here: https://www.elastic.co/guide/en/elasticsearch/reference/1.4/query-dsl-query-string-query.html#query-string-syntax. Elasticsearch uses Lucene under the hood.

Some of the Elasticsearch query syntax has been disabled in order to prevent queries which may damage performance. The disabled features are:

Wildcard searches. You may not put a * into a query string: https://www.elastic.co/guide/en/elasticsearch/reference/1.4/query-dsl-query-string-query.html#_wildcards

Regular expression searches. You may not put an expression between two forward slashes /regex/ into a query string: https://www.elastic.co/guide/en/elasticsearch/reference/1.4/query-dsl-query-string-query.html#_regular_expressions. This is done both for performance reasons and because of the escaping of forward slashes / described above.

Fuzzy Searches. You may not use the ~ notation: https://www.elastic.co/guide/en/elasticsearch/reference/1.4/query-dsl-query-string-query.html#_fuzziness

Proximity Searches. https://www.elastic.co/guide/en/elasticsearch/reference/1.4/query-dsl-query-string-query.html#_proximity_searches

How-To Guide on CRUD API
Creating articles
Documentation for the structure of the JSON documents that you can send to our API is hosted on our Github repository.

If you try to create an article with a DOI or a full-text URL as another one of the articles associated with your account, then the system will detect this as a duplicate. It will overwrite the old article we have with the new data you're supplying via the CRUD Article Create endpoint. It works in the same way as submitting article metadata to DOAJ via XML upload or manual entry with your publisher user account.

Applications - Update Requests
If you wish to submit an application which is intended to provide updated information for an existing Journal you have in DOAJ, then you can submit an Update Request.

An Update Request can be created by sending a new application record via the Application CRUD endpoint, and including the identifier of the Journal it replaces in the "admin.current_journal" field:

    POST /api/applications?api_key=?????

    {
        "admin" : {
            "current_journal" : 1234567890
        },
        "bibjson : { ... }
    }
When you do this, a new application will be created, based on the pre-existing Journal. There are a number of fields that will be ignored when provided during an Update Request, these are:

Title - bibjson.title
Alternative Title - bibjson.alternative_title
Print ISSN - bibjson.identifier type=pissn
Electronic ISSN - bibjson.identifier type=eissn
Contact Name - admin.contact.name
Contact Email - admin.contact.email
If you need to change any of these fields, please contact us.

Once you have created a new Update Request, you can make changes to that via the CRUD endpoint (both Update and Delete) until an administrator at DOAJ picks it up for review. Once it is picked up for review, attempts to update or delete the Update Request will be rejected by the API with a 403 (Forbidden).

API FAQs
Is there an upload limit for uploading articles, or a rate limit?
No, there is no limit set on how many articles you can upload, but we do have a rate limit. See below.

There are two ways to upload articles to DOAJ:

One by one via the Article CRUD API. This allows one article at a time but it should be possible to upload 1-2 per second, or more if you have multiple IP addresses sending them at once.
In batches using the Article Bulk API (only for authenticated users). There are no limits to how many articles are uploaded in a batch. However, processing happens synchronously so you may encounter a timeout based on how long the articles take to process in our system. The timeout is set very high: our server has 10 minutes to respond before the web server closes the connection. Your client may drop the connection sooner, however. Keep the batch sizes small to help mitigate this. We recommend around 600 kilobytes.
There is a rate limit of two requests per second on all API routes. "Bursts" are permitted, which means up to five requests per user are queued by the system and are fulfilled in turn so long as they average out to two requests per second overall.

When making a POST request, do we need to include any of the fields in the admin hash (e.g. in_doaj or upload_id)?
In applications, only the contact subfield is required in the admin section. The full list is handled in our validation structure.

Should language and country be spelled out or can I use codes?
You can use either but using the correct ISO-3166 two-character code is the most robust route. The incoming data is passed to our get_country_code() function which looks up from that list so a name will also work.

How do you identify ISSNs via POST requests?
To identify the correct ISSN, use "https://doaj.org/api/search/journals/issn:XXXX-XXXX" where XXXX-XXXX is the ISSN of your journals.

Do we need the last_updated or created_date to be included?
No, these fields are generated by the system and will be ignored if included.

Should keywords be comma-separated as a single string (e.g. "foo, bar") or separate strings (e.g. ["foo", "bar"])?
As a list of separate strings.

For the link[:content_type] - what are acceptable values?
We expect one of ["PDF", "HTML", "ePUB", "XML"]

Are start_page and end_page required?
In articles these fields are not required. See this list for required fields in article uploads.

Version History
Date changes were made live	Changes
21st August 2025	v4.0.1 - Article API now normalises bibjson.identifier.type to lower-case (e.g. DOI becomes doi), and ignores identifier types which are not explicitly managed by DOAJ (DOIs and ISSNs).


open alex

# API Overview

The API is the primary way to get OpenAlex data. It's free and requires no authentication. The daily limit for API calls is 100,000 requests per user per day. For best performance, [add your email](rate-limits-and-authentication.md#the-polite-pool) to all API requests, like `mailto=example@domain.com`.

## Learn more about the API

* [Get single entities](get-single-entities/)
* [Get lists of entities](get-lists-of-entities/) — Learn how to use [paging](get-lists-of-entities/paging.md), [filtering](get-lists-of-entities/filter-entity-lists.md), and [sorting](get-lists-of-entities/sort-entity-lists.md)
* [Get groups of entities](get-groups-of-entities.md) — Group and count entities in different ways
* [Rate limits and authentication](rate-limits-and-authentication.md) — Learn about joining the [polite pool](rate-limits-and-authentication.md#the-polite-pool)
* [Tutorials ](../additional-help/tutorials.md)— Hands-on examples with code

## Client Libraries

There are several third-party libraries you can use to get data from OpenAlex:

* [openalexR](https://github.com/ropensci/openalexR) (R)
* [OpenAlex2Pajek](https://github.com/bavla/OpenAlex/tree/main/OpenAlex2Pajek) (R)
* [KtAlex](https://github.com/benedekh/KtAlex) (Kotlin)
* [PyAlex](https://github.com/J535D165/pyalex) (Python)
* [diophila](https://pypi.org/project/diophila/) (Python)
* [OpenAlexAPI](https://pypi.org/project/openalexapi/) (Python)

If you're looking for a visual interface, you can also check out the free [VOSviewer](https://www.vosviewer.com/), which lets you make network visualizations based on OpenAlex data:

![](<../.gitbook/assets/Screenshot by Dropbox Capture (1).png>)