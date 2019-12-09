import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import ValidatedLoginForm from './components/ValidatedLoginForm'
import Admin from './components/Admin'
function Home() {
  return (
    <h1>
      Home Page
    </h1>
  )
}

function About() {
  return (
    <h1>
      Admin Page
    </h1>
  )
}

function App() {
  return (
    <main>
      <Switch>
        <Route path="/" component={Home} exact />
        <Route path="/admin" component={ValidatedLoginForm} />
        <Route path="/dashboard" component={Admin} />
      </Switch>
    </main>
  );
}

export default App;
