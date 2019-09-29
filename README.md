# MARS-Dataset
This repository contains the dataset/benchmark related scripts (and data) for the paper "[Maximal Multi-layer Specification Synthesis](https://dl.acm.org/citation.cfm?doid=3338906.3338951)". 

### off-the-shell dataset

The final dataset ready for use is `op_dataset.pkl`. It contains the formatted StackOverflow posts with questions, answers and post statistics (e.g., accepted status, number of stars and up-votes, etc.). For some of the answers that contain code snippets, we also parse them using a simple parser to extract the program syntax tree structures and sketches. While in order to feed the data into a sequence-to-sequence model, you may need to run an NLP pre-processing pipeline that fits your need by yourself.

Use the `pickle` library to load  `op_dataset.pkl`. The data structure is shown as below:

```python
op_dataset = {
  "DPLYR": [ # key word used to search for posts
    (
      # (dict) meta data for a post
      {
        "url": str, # the original url of this post
        "vote": int, # the number of votes of the question
        "ansr": int, # the number of answers of the question
        "acpt": int, # the number of accepted answers of this question
        "view": int, # the number of views of this question
        "title": str, # the title of this post
        "tags": list of str, # a list of tags of this question
        "time": float, # timestamp of this question
      },
      
      # (list) question data
     	[
        # the question data is segmented
        # every segment is attached with an int indicating whether the segment
        # is string(0) or code(1)
        (0,txt),(1,code),...
      ],
      
      # (list) answer data
      # each answer is a dict
      [
        {
          "acpt": bool, # whether the answer is accepted or not
          "vote": int, # number of up-votes of this answer
          "ansr": [ # the answer in segmented form
            (0,txt),(1,code),...
          ],
          "ansr_parsed": list of dict, # syntax trees of code snippets in the answer
          "ansr_op": list of tuple, # extracted sketches from the answer
        },
        {...},
        {...},
        ...
      ],
    ),
    (...),
    (...),
    ...
  ],
  "TIDYR": [ # key word used to search for posts
    ...
  ]
}
```

The benchmarks we used are originally from [Morpheus](https://utopia-group.github.io/morpheus/). You can find a more detailed version from its official github page. Our dataset provides the benchmarks with more dimensions (e.g., with original problem descriptions) compared to the original Morpheus benchmarks. The corresponding urls for each benchmarks can be found in `benchmark_urls.py`.

> Notice: You may have to manually filter out the Morpheus benchmarks from the dataset if you want to deploy a statistical learning framework using the dataset as training set.

### script usage

We also include scripts that generate the dataset. You can extend/modify the functions of the scripts. Here are the general data generation procedure (in Python 3).

1. `python meta_scraper.py`: This will initiate searches on StackOverflow with keywords "dplyr" and "tidyr", collect result post urls and store them into `meta_dataset.pkl`.
2. `python content_scraper.py`: This will scrape the related contents from the given url file generated from the previous step, and store them into `dataset.pkl`.
3. `python code_parser.py`: This will call a simple parser to extract syntax trees from the scrapped code snippets.
4. `python op_extractor.py`: This will recognize the valid components that compose a valid sketch from a syntax tree generated from the previous step.

### citation

If you find our work useful in your research, please consider citing:

```
@inproceedings{Chen:2019:MMS:3338906.3338951,
 author = {Chen, Yanju and Martins, Ruben and Feng, Yu},
 title = {Maximal Multi-layer Specification Synthesis},
 booktitle = {Proceedings of the 2019 27th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering},
 series = {ESEC/FSE 2019},
 year = {2019},
 isbn = {978-1-4503-5572-8},
 location = {Tallinn, Estonia},
 pages = {602--612},
 numpages = {11},
 url = {http://doi.acm.org/10.1145/3338906.3338951},
 doi = {10.1145/3338906.3338951},
 acmid = {3338951},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Max-SMT, machine learning, neural networks, program synthesis},
}
```

