"use client";
import {useEffect, useState} from "react";

export default function Home() {
  const [count, setCount] = useState<number  | null>(null);

  useEffect(() => {
    // Appel à l'API pour récupérer le nombre de tâches
    fetch("http://127.0.0.1:8090/rest/todo/Jonathan/count_tasks")
      .then((response) => response.json())
      .then((data) => setCount(data.count)) // Assure-toi que la réponse a un champ 'count'
      .catch((error) => {
        console.error("Erreur lors de la récupération des tâches :", error);
        setCount(0); // Valeur par défaut en cas d'erreur
      });
  }, []);

  return (
    <div>
      {count !== null ? `Il y a ${count} tâche(s) en attente` : "Chargement..."}
    </div>
  );
}
