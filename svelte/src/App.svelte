<script>
import Login from './components/Login.svelte'
import {Router, Route} from 'svelte-routing'
import Signup from './components/Signup.svelte'
</script>
<Router>
    <Route path= '/Login' component={Login} />
    <Route path='/Signup' component={Signup} />
</Router>
<Login />