<script>
import Login from './components/Login.svelte'
import Homepage from './components/Homepage.svelte'
import {Router, Route} from 'svelte-routing'
import {signedin} from './components/Signup.svelte'
import {loggedin} from './components/Login.svelte'
console.log($loggedin)
console.log($signedin)
let r=sessionStorage.getItem("Valid")
if(r){
    loggedin.set(true)
    signedin.set(true)
}
import Signup from './components/Signup.svelte'
</script>

<Router>
    <Route path= '/Login' component={Login} />
    <Route path='/Signup' component={Signup} />
</Router>
{#if $signedin==false && $loggedin==false}

<Login />
{:else}
<Homepage />
{/if}
