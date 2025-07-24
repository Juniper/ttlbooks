# Markdown user-guide

**This is the markdown formatting validated to be well rendered to Static HTML along with the PDF exportation. Please only use these validated formats**

### Markdown comments

```markdown
<!-- Comments are written this way - not published -->
<!-- shortcut for comments: alt + shift + a -->
```

### Paragraph

Always add a space after a punctuation mark to return to a new line.
To create a new paragraph, add two spaces at the end of the line.

Here is my new paragraph is this one. 

### Title hierarchy

You may add numbering if needed:

```markdown
# 1.    Title level 1
## 1.1. Title level 2
### 1.1.1. Title level 3
#### Title level 4
##### Title level 5
###### Title level 6
```

# Result:

# 1.    Title level 1
## 1.1. Title level 2
### 1.1.1. Title level 3
#### Title level 4
##### Title level 5
###### Title level 6

### Bold text

```markdown
**my bold text**
```

# Result:

**my bold text**

### Italic text

```markdown
*my italic text*
```

# Result:

*my italic text*

### Create a note

```
> This is a note...
```

# Result:

> This is a note...

### Code or CLI output

````markdown
```plaintext
regress@rtme-mx-25> show version 
Hostname: rtme-mx-25
Model: mx480
Family: junos
Junos: 25.2I-20250303.0.2029
```
````

# Result:

```plaintext
regress@rtme-mx-25> show version 
Hostname: rtme-mx-25
Model: mx480
Family: junos
Junos: 25.2I-20250303.0.2029
```

### Links

External link:

```markdown
[external-link-name](https://www.example.com)
```

# Result:

[external-link-name](https://www.example.com)

Internal link (to a specific title):

```markdown
[internal-link-name](#title-level-1)
```

# Result:

[internal-link-name](#title-level-1)

### Internal reference

```mardown
Markdown is a lightweight markup language designed to be easy to read and write. It allows users to format text using simple syntax while keeping the document plain and readable. 

Your internal reference: 

[Internal-reference-name](#anchorX)

One of the key benefits of Markdown is its versatility. It can be converted to various formats such as HTML, PDF, and even Word documents. This makes it popular for documentation, note-taking, and content creation.  

Your ANCHOR: 

<a id="anchorX"></a>

With support for headings, lists, tables, and code blocks, Markdown simplifies content organization without requiring complex formatting tools.  
```

# Result:

Markdown is a lightweight markup language designed to be easy to read and write. It allows users to format text using simple syntax while keeping the document plain and readable. 

**Your internal reference:**

[Internal-reference-name](#anchorX)

One of the key benefits of Markdown is its versatility. It can be converted to various formats such as HTML, PDF, and even Word documents. This makes it popular for documentation, note-taking, and content creation.  

**Your ANCHOR:**

<a id="anchorX"></a>

With support for headings, lists, tables, and code blocks, Markdown simplifies content organization without requiring complex formatting tools.  

### Images

```markdown 
The caption is not rendered by markdown but will be used during the PDF rendering to add figure caption - numbering will be managed by the tool. 

![image-caption-for-pdf](docs/images/favicon.ico)
````

# Result:

![image-caption-for-pdf](docs/images/favicon.ico)

### Footnote

```markdown
my text that needs footnote[^1]

and on the bottom of the md file: 

[^1]: Put this to the end of the document, the footnote will be listed like this. Rendering will put the footnote on the right page - don't care about that.
```

# Result:

my text that needs footnote[^1]

and on the bottom of the md file: 

[^1]: Put this to the end of the document, the footnote will be listed like this. Rendering will put the footnote on the right page - don't care about that.

### Tables

```markdown
| Header1  | header2 | header3  |
|:-|:-|:-|
| cell 1   | cell 2    | cell 3    |
| cell 1   | cell 2    | cell 3    |
| cell 1   | cell 2    | cell 3    |

: This is table caption not render by markdown but will be for PDF 
```

# Result:

| Header1  | header2 | header3  |
|:-|:-|:-|
| cell 1   | cell 2    | cell 3    |
| cell 1   | cell 2    | cell 3    |
| cell 1   | cell 2    | cell 3    |

: This is table caption not render by markdown but will be for PDF

More info: https://tabletomarkdown.com/convert-spreadsheet-to-markdown/

### List

```markdown
This is a list:

- elem1
- elem2
- elem3
```

# Result:

This is a list:

- elem1
- elem2
- elem3

### Latex math Formula

One formula: 

```markdown
$$
\frac{10^{6}}{\text{policer clock tick}_{\mu s}} = \frac{10^{6}}{\text{policer tick} \cdot 2^{5R}}
$$
```

# Result:

$$
\frac{10^{6}}{\text{policer clock tick}_{\mu s}} = \frac{10^{6}}{\text{policer tick} \cdot 2^{5R}}
$$

Help: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions
