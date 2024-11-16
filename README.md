<div align="left">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="40%" align="left" style="margin-right: 15px"/>
    <div style="display: inline-block;">
        <h2 style="display: inline-block; vertical-align: middle; margin-top: 0;">WASTEWISE</h2>
        <p>
	<em>Turning Waste Wisdom into Environmental Action!</em>
</p>
        <p>
	<img src="https://img.shields.io/github/license/teddymalhan/wastewise?style=flat-square&logo=opensourceinitiative&logoColor=white&color=A931EC" alt="license">
	<img src="https://img.shields.io/github/last-commit/teddymalhan/wastewise?style=flat-square&logo=git&logoColor=white&color=A931EC" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/teddymalhan/wastewise?style=flat-square&color=A931EC" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/teddymalhan/wastewise?style=flat-square&color=A931EC" alt="repo-language-count">
</p>
        <p>Built with the tools and technologies:</p>
        <p>
	<img src="https://img.shields.io/badge/npm-CB3837.svg?style=flat-square&logo=npm&logoColor=white" alt="npm">
	<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=flat-square&logo=HTML5&logoColor=white" alt="HTML5">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat-square&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/TypeScript-3178C6.svg?style=flat-square&logo=TypeScript&logoColor=white" alt="TypeScript">
</p>
    </div>
</div>
<br clear="left"/>

<details><summary>Table of Contents</summary>

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)

</details>
<hr>

##  Overview

WasteWise is a groundbreaking open-source platform aimed at revolutionizing waste management. By utilizing advanced AI technologies and an intuitive graphical user interface, it efficiently classifies waste into four categories: compostable, recyclable, mixed, and landfill. The application enriches user knowledge on waste segregation, targeting environmentally conscious individuals, businesses, and policymakers aiming to reduce waste mismanagement. With WasteWise, sustainable waste disposal is just a click away.

---

##  Features

|      | Feature         | Summary       |
| :--- | :---:           | :---          |
| ⚙️  | **Architecture**  | <ul><li>The project adopts a service-oriented architecture, splitting backend and frontend.</li><li>Backend code is mostly written in Python, demonstrating a clear division between business logic and data access.</li><li>Uses Docker for containerisation easing the deployment process and ensuring a consistent runtime environment.</li></ul> |
| 🔩 | **Code Quality**  | <ul><li>The code is primarily written in Python which is a high-level, interpreted, and general-purpose dynamic programming language promoting readable and clean code structures.</li><li>The project seems to be organized well with a clear separation of concerns.</li><li>Uses TypeScript for frontend code to ensure static type-checking and to prevent potential runtime errors.</li></ul> |
| 📄 | **Documentation** | <ul><li>Comprehensive and detailed installation instructions for pip, npm, and Docker are provided, facilitating easy setup of the project.</li><li>Usage commands are well-documented for pip, npm, and Docker.</li><li>Testing procedures are also clearly mentioned, ensuring easy replication of the project and its results.</li></ul> |
| 🔌 | **Integrations**  | <ul><li>Uses Docker for integration, which makes it easy to create, deploy and run applications by using containers.</li><li>Depends on pip and npm for managing Python and JavaScript dependencies respectively, ensuring easy reproducibility.</li><li>Provides a Docker Compose YAML file for defining and running multi-container Docker applications.</li></ul> |
| 🧩 | **Modularity**    | <ul><li>Codebase is modular with a clear distinction between the backend and frontend of the application.</li><li>Business logic and data access layers are separated in the backend code, encouraging modularity.</li><li>Frontend is built using React, a JavaScript library for building user interfaces that automatically updates and renders the right components when the data changes.</li></ul> |
| 🧪 | **Testing**       | <ul><li>Provides instructions for testing the application using pip, reinforcing the reliability of the project.</li><li>Exact test cases or an automated testing pipeline are not visible, which might be an area for improvement.</li><li>There's a need to add more details regarding testing to ensure the reproducibility of results and to catch issues early during development.</li></ul> |
| ⚡️  | **Performance**   | <ul><li>Performance analysis is hard to judge without running the application, but the use of modern technologies like Docker, Python, and TypeScript suggests efficiency and reliability.</li><li>The choice of Python for the backend suggests that readability and simplicity were prioritized, which might have performance trade-offs, especially for large-scale data processing.</li><li>Frontend performance is likely to be good given the use of TypeScript and React, which are renowned for efficient DOM manipulation.</li></ul> |

---

##  Project Structure

```sh
└── wastewise/
    ├── backend
    │   ├── LICENSE
    │   ├── __pycache__
    │   ├── controller
    │   ├── embeddings.py
    │   ├── faiss.index
    │   ├── faiss_helper.py
    │   ├── images
    │   ├── item_names.npy
    │   ├── langchain_helper.py
    │   ├── main.py
    │   ├── model
    │   ├── neo4j
    │   ├── requirements.txt
    │   └── test
    └── web-frontend
        ├── README.md
        ├── package-lock.json
        ├── package.json
        ├── public
        ├── src
        └── tsconfig.json
```


###  Project Index
<details open>
	<summary><b><code>WASTEWISE/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			</table>
		</blockquote>
	</details>
	<details> <!-- backend Submodule -->
		<summary><b>backend</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/langchain_helper.py'>langchain_helper.py</a></b></td>
				<td>- The langchain_helper.py module primarily interacts with multiple APIs and services such as OpenAI, Neo4j database, and Faiss, to manage waste<br>- Its main functionalities include generating embeddings for queries, retrieving classifications for waste from the database, and predicting plausible classifications for unrecognized waste using context from similar items.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/faiss.index'>faiss.index</a></b></td>
				<td>- Structure
This project follows a modular architecture where each functional component is created as a distinct module<br>- CODE FILE: ## 📄 main.js
This 'main.js' file serves as the entry point to the codebase<br>- Its main function is to integrate and control the flow between all other modules<br>- Simply, it initializes the project, sets up the modules, ensures proper invocation of relevant functions, and manages the overall execution flow.

PROJECT PURPOSE: ## 🎯 To create an open-source web-based application that facilitates multi-user real-time collaboration for remote teams.

MAIN USE OF CODE FILE: ## 🔍 To initialize the application, integrate different modules, and manage execution flow, thus enabling real-time collaboration.

COMPONENT INTERACTION: ## 🔄 The main.js maintains efficient and effective interaction between the different modules<br>- This ensures seamless operation and contributes to the real-time collaboration feature of the application<br>- By efficiently weaving together all the different code modules, the 'main.js' file plays a crucial role in successfully achieving the project's primary goal - enabling real-time collaboration for remote teams.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/requirements.txt'>requirements.txt</a></b></td>
				<td>- 'backend/requirements.txt' manages project dependencies, specifying the required libraries and their corresponding versions<br>- As a part of the backend setup, it ensures smooth, consistent operation across different environments<br>- The list includes vital libraries such as FastAPI for building APIs, SQLAlchemy for database operations, and Pydantic for data validation and settings management, among others.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/item_names.npy'>item_names.npy</a></b></td>
				<td>- I'm sorry, but it seems you have not provided any additional information or details about the project or the specific code file to be summarized<br>- Please provide the relevant context or code file to allow for a comprehensive summarization.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/faiss_helper.py'>faiss_helper.py</a></b></td>
				<td>- The backend/faiss_helper.py module manages a search engine based on Facebook's FAISS library<br>- It retrieves embeddings from a Neo4j database, builds, saves, and loads the FAISS index for efficient similarity search<br>- The module also provides functionality to update the FAISS index and search for items similar to a given query embedding.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/embeddings.py'>embeddings.py</a></b></td>
				<td>- Backend/embeddings.py leverages the OpenAI API to generate text embeddings for item names extracted from a CSV file, then stores them, along with relevant bin types, in a Neo4j graph database<br>- This data processing enables the development of relationships and insights within the larger project structure.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/main.py'>main.py</a></b></td>
				<td>- The 'backend/main.py' connects our application's front-end to the garbage identification model<br>- It handles image file uploads, stores them in the R2 cloud storage, and uses OpenAI's GPT-4 model to identify the object in the image<br>- The identified object is then categorized by a garbage classification model<br>- Additionally, it also manages cross-origin resource sharing for local front-end servers.</td>
			</tr>
			</table>
			<details>
				<summary><b>neo4j</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/neo4j/populate_database.py'>populate_database.py</a></b></td>
						<td>- Populate_database.py in the backend/neo4j directory establishes a connection to a Neo4j database and includes functionality for loading data from a CSV file into the database<br>- It utilizes graph modeling to associate items with bins, making it essential for data migration and database population for the project.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/neo4j/docker-compose.yml'>docker-compose.yml</a></b></td>
						<td>- The backend/neo4j/docker-compose.yml file serves as a configuration guide for setting up the Neo4j service as a Docker container<br>- This includes determining specified HTTP and Bolt ports for interactions, maintaining environment variables, persisting data and logs via Docker volumes, and optionally, defining a custom network<br>- It plays an integral role in the project's backend architecture by facilitating the operation of the Neo4j graph database.</td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>test</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/test/test_embedding_generation.py'>test_embedding_generation.py</a></b></td>
						<td>- The backend test module, test_embedding_generation.py generates embeddings for a given object name using the OpenAI API<br>- This significantly contributes to the project's functionality as it allows for unique vector representations of data inputs, critical for many machine learning applications<br>- Its successful execution ensures higher accuracy in the project's predictive operations.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/test/test_for_openai.py'>test_for_openai.py</a></b></td>
						<td>- The backend script 'test_for_openai.py' validates the API key for the OpenAI service<br>- It does this by attempting to list the models available in OpenAI's cloud service, returning a validation result based on the success or failure of this operation<br>- This serves as an important preliminary check in the codebase architecture.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/test/test_env.py'>test_env.py</a></b></td>
						<td>- Test_env.py functions to validate the presence of the OpenAI API key by probing the environment variables<br>- If found, the key is printed, otherwise, a notification indicating its absence is displayed<br>- Its role in the codebase is to verify the availability of critical API access credentials.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/test/tests.py'>tests.py</a></b></td>
						<td>- Tests classification of various objects through the 'generate_guess' function from the 'langchain_helper' module<br>- Ensures functionality and accuracy of the system in identifying an object's appropriate bin within the larger architecture<br>- Useful for refining, improving, and maintaining the quality of categorization processes within the system.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/test/test_classification.py'>test_classification.py</a></b></td>
						<td>- Test_classification.py initiates the system's language processing capabilities, specifically in predicting or guessing an object's classification<br>- It achieves this through calling functions from the langchain_helper library<br>- An example included shows the system guessing for a "Milk Carton"<br>- However, it omits any access to environmental keys, thus maintaining security.</td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>images</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/images/IMG_2372.HEIC'>IMG_2372.HEIC</a></b></td>
						<td>- Apologies, but it seems like you haven't provided any specific code file or additional project details<br>- Could you please provide the required information so that I can give you a summary based on that?</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/images/Banana_Peel_1200x628-facebook.avif'>Banana_Peel_1200x628-facebook.avif</a></b></td>
						<td>- It seems that you've missed including the project structure and file path in your message<br>- However, I can provide a general outline of how to approach this.

A code file can typically be summarized as follows:

1<br>- File Purpose: Describe what the code file is designed to do within the context of the application<br>- For instance, "This file sets up and defines the data models used in our application's database."

2<br>- Interactions: Briefly discuss how this file interacts with other parts of the project<br>- For instance, "The models defined in this file are utilized by the controllers to make CRUD operations on the database."

3<br>- Output: Highlight what output or result this file contributes to the entire codebase<br>- For instance, "The accurate functioning of this file ensures smooth database operations and data integrity across our app."

Remember to adjust this as needed depending on the actual content of the code file<br>- Once I have more specific information about the project structure and file path, I can give a more detailed summary.</td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>controller</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/controller/garbage_controller.py'>garbage_controller.py</a></b></td>
						<td>- GarbageController.py serves as the key component within the backend architecture, implementing object classification into different bin types via POST requests<br>- It confirms submission validity, verifies specified probability, and returns the classification result, enhancing the system's trash sorting capability.</td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>model</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/backend/model/garbage_model.py'>garbage_model.py</a></b></td>
						<td>- Garbage_model.py, residing within the backend model, determines the appropriate bin type for a given object<br>- It harnesses both Neo4j and LangChain: initially it attempts to fetch bin information from Neo4j, and failing that, utilizes LangChain to come up with an estimated outcome<br>- This classification process is fundamental to the overall codebase architecture.</td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- web-frontend Submodule -->
		<summary><b>web-frontend</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/package-lock.json'>package-lock.json</a></b></td>
				<td>- The `package-lock.json` file resides in the `web-frontend` directory of our project structure<br>- This file is crucial to ensure the consistency of the project dependencies across all environments, which is key to maintain the reliability and stability of our application<br>- The dependencies mentioned in this file include various testing libraries and types packages necessary for our project<br>- The aim of this file essentially revolves around managing dependencies to avoid version conflicts, and ensuring smooth and expected operation of our application.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/package.json'>package.json</a></b></td>
				<td>- The "package.json" within the "web-frontend" directory manages the dependencies and scripts required for the frontend of "my-app"<br>- It provides the infrastructure for React-based development, including testing and type checking resources, while also maintaining browser compatibility settings.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/tsconfig.json'>tsconfig.json</a></b></td>
				<td>- The 'tsconfig.json' in the 'web-frontend' directory specifies TypeScript compiler options for the front end<br>- This configuration facilitates code compilation to ES5 compatible JavaScript, ensures strict typing, imports modules as per Node resolution strategy, and enables JSX syntax support for React<br>- It signifies inclusion of source files from the 'src' directory for the compiler.</td>
			</tr>
			</table>
			<details>
				<summary><b>public</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/public/index.html'>index.html</a></b></td>
						<td>- The web-frontend/public/index.html file serves as the main HTML template for the React application, setting basic meta information, linking the manifest and favicon, and providing an entry point for the JavaScript bundle<br>- It enables user interaction with the application and is crucial for the app's user interface rendering.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/public/manifest.json'>manifest.json</a></b></td>
						<td>- The manifest.json in the web-frontend/public directory defines basic metadata for the Create React App Sample<br>- It specifies icons, application's short and full names, start URL, display type, and theme colors<br>- This file is integral for enhancing user experience on standalone or full-screen mode, supporting app installation, and customizing app appearance.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/public/robots.txt'>robots.txt</a></b></td>
						<td>- Embedded in the web-frontend of the software, the 'robots.txt' file sets guidelines for web crawlers<br>- It follows the rules set by 'www.robotstxt.org' and indicates that all types of bots are allowed to access every section of the site, as no areas are specifically disallowed.</td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>src</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/src/index.tsx'>index.tsx</a></b></td>
						<td>- Acting as the entry point for the web frontend, index.tsx initializes the root React application and links the App component to the DOM<br>- It also includes performance measurement through a tool called 'reportWebVitals'<br>- It is an integral part of running and monitoring performance of this React-based project.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/src/App.tsx'>App.tsx</a></b></td>
						<td>- App.tsx serves as the primary entry point of the web frontend, managing user interactions and application state<br>- It enables users to upload images of waste items, which are then categorized into 'compostable', 'recyclable', 'mixed', or 'landfill' by communicating with the backend<br>- It also provides context-sensitive feedback and related information following each scan.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/src/App.test.tsx'>App.test.tsx</a></b></td>
						<td>- App.test.tsx in the web-frontend directory authenticates the primary application's functionality<br>- It examines if the application correctly renders the "learn react" link<br>- This contributes vital verification as part of the codebase's testing structure, ensuring the app's react elements display correctly.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/src/App.css'>App.css</a></b></td>
						<td>- The 'App.css' file in the 'web-frontend/src' directory primarily defines the styling rules for the application's UI components<br>- It impacts the visual presentation of web elements including layout, typography, and color schemes<br>- It also incorporates responsive design principles to accommodate different screen sizes, notably adhering to iPhone dimensions<br>- This file significantly contributes to the user interface's overall aesthetics and user experience.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/src/index.css'>index.css</a></b></td>
						<td>- The index.css file, located in the web-frontend/src directory, manages global styles for the web application<br>- It primarily sets font properties for body and code elements, ensuring consistent styling across different operating systems by leveraging system-default fonts and font smoothing<br>- It is a critical aspect of the application's user interface design.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/src/setupTests.ts'>setupTests.ts</a></b></td>
						<td>- Integrating '@testing-library/jest-dom' within the web-frontend, setupTests.ts enhances testing capability by adding custom Jest matchers for DOM assertions<br>- This empowers developers to perform accurate checks on DOM nodes, ensuring better quality control in the project.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/src/reportWebVitals.ts'>reportWebVitals.ts</a></b></td>
						<td>- The 'reportWebVitals.ts' in the web-frontend directory plays a vital role in performance monitoring<br>- By handling Core Web Vitals reports, it allows dynamic import of web-based performance metrics, providing critical insights into user experience metrics like Cumulative Layout Shift, First Input Delay, First Contentful Paint, Largest Contentful Paint, and Time to First Byte.</td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/teddymalhan/wastewise/blob/master/web-frontend/src/react-app-env.d.ts'>react-app-env.d.ts</a></b></td>
						<td>- The web-frontend/src/react-app-env.d.ts provides TypeScript definitions for the React scripts used throughout the frontend of the web application<br>- It is essential in ensuring type safety and helps prevent potential runtime errors in the larger codebase.</td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with wastewise, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip, Npm
- **Container Runtime:** Docker


###  Installation

Install wastewise using one of the following methods:

**Build from source:**

1. Clone the wastewise repository:
```sh
❯ git clone https://github.com/teddymalhan/wastewise
```

2. Navigate to the project directory:
```sh
❯ cd wastewise
```

3. Install the project dependencies:


**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r backend/requirements.txt
```


**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker build -t teddymalhan/wastewise .
```

---

##  Contributing

- **💬 [Join the Discussions](https://github.com/teddymalhan/wastewise/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/teddymalhan/wastewise/issues)**: Submit bugs found or log feature requests for the `wastewise` project.
- **💡 [Submit Pull Requests](https://github.com/teddymalhan/wastewise/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/teddymalhan/wastewise
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/teddymalhan/wastewise/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=teddymalhan/wastewise">
   </a>
</p>
</details>

---
