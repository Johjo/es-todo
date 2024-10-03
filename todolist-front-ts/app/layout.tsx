"use client";
import Image from "next/image";
import type {ReactNode} from "react";
import {StoreProvider} from "./StoreProvider";
import {Nav} from "./components/Nav";

import "./styles/globals.css";
import styles from "./styles/layout.module.css";
import {DependenciesList, DependenciesProvider, WhichTaskQuery, WhichTaskResponse} from "@/app/controller";

interface Props {
  readonly children: ReactNode;
}

class TodolistReaderFromBack implements WhichTaskQuery {
  async whichTask(): Promise<WhichTaskResponse> {
    const response: Response = await fetch("http://127.0.0.1:8090/rest/todo/Jonathan/which_task");

    if (!response.ok) {
      throw new Error(`Erreur lors de la récupération des tâches : ${response.statusText}`);
    }

    const data = await response.json();
    return {tasks: data.fvpTasks};
  }
}

const dependencies : DependenciesList = {
  todolistReaderForRefreshTodolist(): WhichTaskQuery {
    return new TodolistReaderFromBack();
  }

};

export default function RootLayout({ children }: Props) {
  return (
    <StoreProvider>
      <DependenciesProvider dependencies={dependencies}>
      <html lang="en">
        <body>
          <section className={styles.container}>
            <Nav />

            <header className={styles.header}>
              <Image
                src="/logo.svg"
                className={styles.logo}
                alt="logo"
                width={100}
                height={100}
              />
            </header>

            <main className={styles.main}>{children}</main>

            <footer className={styles.footer}>
              <span>Learn </span>
              <a
                className={styles.link}
                href="https://reactjs.org"
                target="_blank"
                rel="noopener noreferrer"
              >
                React
              </a>
              <span>, </span>
              <a
                className={styles.link}
                href="https://redux.js.org"
                target="_blank"
                rel="noopener noreferrer"
              >
                Redux
              </a>
              <span>, </span>
              <a
                className={styles.link}
                href="https://redux-toolkit.js.org"
                target="_blank"
                rel="noopener noreferrer"
              >
                Redux Toolkit
              </a>
              <span>, </span>
              <a
                className={styles.link}
                href="https://react-redux.js.org"
                target="_blank"
                rel="noopener noreferrer"
              >
                React Redux
              </a>
              ,<span> and </span>
              <a
                className={styles.link}
                href="https://reselect.js.org"
                target="_blank"
                rel="noopener noreferrer"
              >
                Reselect
              </a>
            </footer>
          </section>
        </body>
      </html>
      </DependenciesProvider>
    </StoreProvider>
  );
}
