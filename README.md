# Metamorphic DAO

<p align="center">
  <img src="https://github.com/akhtarshahnawaz/Metamorphic-DAO/blob/main/cover.jpeg" />
</p>

Check out the associated presentation here: [Presentation](https://github.com/akhtarshahnawaz/Metamorphic-DAO/blob/main/Presentation.pdf)

Current state of Decentralised Autonomous organisations is really grave. Most of DAO implementation are basically just a piece voting platform where people who are in DAO vote on governance proposals with very limited automation or flexibility. Most DAOs are implememnted on EVM where they are limited by capabilities of EVM. They can't do complicated decision making or any AI driven task. Also the execution logic of most of DAOs is really rigid and difficult to change once they are established. Some part of it can be changed using proxy contract, however even then their execution logic is limited by the platform they run on and most blockchain platform have very limited capability in case of processing and memory.

That was all in past. A new layer 2 app specific rollup chain allows us to build decentralied apps directly on Risk V machine with linux as backend. That allows us to run application of any complexity and memory requirements on them.

I believe that DAOs execution logic are like constitutions of country i.e. they provide rules which govern the DAO. and just they way the constitution of a country needs update from time to time through ammendments by political process of time, similarly the execution logic of DAO should be melleable i.e. we should be able to change them whenever required based on ammendment proposals and governance process.

Therefore I used Cartesi platform to build a new type of DAO. In this DAO, all the execution logic of DAO is melleable through governance process. This means that anyone can propose a new code for runtime logic of the DAO, and if enough DAO members agree then the code could be automatically integrated into runtime logic of the DAO. This allows continuous evolution of the DAO runtime logic through governance process.

Cartesi machine allows to run high level softwares and packages for example AI and machine learning toolkits in Python. The runtime logic of this DAO can be supplemented with AI and ML to give deep insights, more automated governance and complex governance mechanism like different voting mechanisms eg quadratic voting etc

I am creating a presentation to showcase my DAO product build on top cartesi. based on the information I have provided, create content to put in power point slides and github readme. Also add a slight philosophical tone to the content

**How it's Made**

The DAO is uses SQLite backend in Cartesi to store the information and runtime logic of the DAO. Whenever someone proposes a new runtime logic, it is stores as a runtime amendment proposal code, and people can vote on that code choosing whether to make it part of the DAO's main runtime or not. If the proposal is passed, the proposed code is moved to the codebase of DAO, and DAO members can then interact with this new code base.

The proposed code can be as complex as the situation requires (thanks to cartesi). One can import python AI and machine learning libraries like sklearn and tensorflow and propose code including these libraries to make the DAO more autonomous and generate useful insights and metrics through AI driven methods.

**How to run the rollup chain**

The application is compiled as a docker container. You can run the code either in host mode or production mode.

To run in production mode, you need to run:

```
./bake.sh
./run.sh
```

which will bake and build the container and then run it in production.

To run in host mode for development purposes, you can run:

```
./run_hostmode.sh
./run_python_hostmode.sh
```

The `run_hostmode.sh` will run the container in hot reload mode, and then we run the backend logic separately using the second command

**How to interact with the application**
Due to limited time, I didn't manage to make the frontend of the project. Therefore the frontend is implemented as a jupyter notebook file to interact with the rollup chain and the main blockchain. To interact with the application, open `Interaction Console.ipynb` in jupyter terminal and then follow the workflow given in the notebook.
