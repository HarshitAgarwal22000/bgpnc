<script>
import Login from './components/Login.svelte'
import Homepage from './components/Homepage.svelte'
import {Router, Route} from 'svelte-routing'
import {signedin} from './components/Signup.svelte'
import {loggedin} from './components/Login.svelte'
console.log(loggedin)
import Signup from './components/Signup.svelte'
</script>

<Router>
    <Route path= '/Login' component={Login} />
    <Route path='/Signup' component={Signup} />
</Router>
{#if signedin==false && loggedin==!true}
<div>{signedin, loggedin}</div>
<Login />
{:else}
<Homepage />
{/if}
