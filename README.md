| 2021 DevNet Create<br />Just Say No To Visio | ![TS30-claudiadeluna_final](images/TS30-claudiadeluna_final.jpg) |
| -------------------------------------------- | ------------------------------------------------------------ |

[Just say No to Visio DevNet Create Video on YouTube](https://youtu.be/6qDTF-rdnI0?si=wkbTAXSuuikK6NSH)

### Documentation as Code

Most of the diagraming modules in Python which I've found useful leverage [Graphviz](https://graphviz.org/about/) and the [DOT language.](https://graphviz.org/doc/info/lang.html)

[Graphviz](https://pypi.org/project/graphviz/)

[The DOT Language](https://graphviz.org/doc/info/lang.html)

[Pygraphviz](https://pygraphviz.github.io)

[Networkx](https://networkx.org/)

[Diagrams](https://github.com/mingrammer/diagrams)

[Introducing Diagrams: Diagram as Code](https://medium.com/better-programming/diagrams-diagram-as-code-56fec222cdf6)

[Pillow (PIL Fork)](https://pillow.readthedocs.io/en/stable/)



### Current State Diagram

Script to quickly draw CDP Neighbors of a given device.

- From saved show command output
- From a device real-time



### Creating Your Environment

Install Graphviz Application
https://graphviz.gitlab.io/download/

Using latest Python 3.10
```bash
% python -V
Python 3.10.14
```

```bash
% dot -V
dot - graphviz version 12.2.1 (20241206.2353)
```

```python
pip install --upgrade pip

pip install -r requirements.txt

# Highlighted Modules
pip install diagrams
pip install textfsm
pip install Pillow
pip install pandas
pip install "scrapli[textfsm]"
pip install python_dotenv
pip install pygraphviz

```

```angular2
claudia@Claudias-iMac vEnvs % brew list --formula | grep graphviz
graphviz
claudia@Claudias-iMac vEnvs % brew search graphviz
==> Formulae
graphviz ✔
claudia@Claudias-iMac vEnvs % brew info graphviz
graphviz: stable 2.44.1 (bottled), HEAD
Graph visualization software from AT&T and Bell Labs
https://www.graphviz.org/
/usr/local/Cellar/graphviz/2.44.1 (506 files, 18MB) *
  Poured from bottle on 2020-09-20 at 10:51:08
From: https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/graphviz.rb
License: EPL-1.0
==> Dependencies
Build: autoconf ✔, automake ✘, pkg-config ✔
Required: gd ✔, gts ✔, libpng ✔, librsvg ✘, libtool ✔, pango ✘
==> Options
--HEAD
	Install HEAD version
==> Analytics
install: 28,467 (30 days), 104,315 (90 days), 542,305 (365 days)
install-on-request: 22,838 (30 days), 85,298 (90 days), 426,276 (365 days)
build-error: 0 (30 days)
claudia@Claudias-iMac vEnvs %
```



### Clone this Repository

Now that you have your working environment, make sure you have cloned this repository.



### Handy Links

Cloud Based Drawing 

https://developer.nulab.com/docs/cacoo/#

https://www.lucidchart.com/pages/api_documentation



### Reference Material

[Diagrams · Diagram as Code](https://diagrams.mingrammer.com/)

[Create Beautiful Architecture Diagrams with Python | by Dylan Roy](https://towardsdatascience.com/create-beautiful-architecture-diagrams-with-python-7792a1485f97)

[Introducing Diagrams](https://medium.com/nerd-for-tech/introducing-diagrams-55b16fa805b9)

https://github.com/carlmontanari/scrapli#textfsmntc-templates-integration



### Icons

Icons provided by Icons8
https://icons8.com/



### Fonts

Dustismo font provided by [Font Squirrel](https://www.fontsquirrel.com/fonts/dustismo)

Liberation Sans font provided by [FontMirror(]https://www.fontmirror.com/liberation-sans)



## Licensing

This code is licensed under the BSD 3-Clause License. See [LICENSE](LICENSE) for details.

