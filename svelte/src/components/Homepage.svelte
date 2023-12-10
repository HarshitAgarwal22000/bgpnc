<script context="module">
    import {loggedin} from './Login.svelte'
    import { writable } from 'svelte/store';
    import {tok} from './Login.svelte'

</script>
<script>
    import {onMount} from 'svelte'
    import {tick} from 'svelte/internal'
    onMount(async()=>{
        let tok=sessionStorage.getItem("Valid")
        let user=sessionStorage.getItem("User")
        const re=await fetch(`http://localhost:8000/interfaces/${user}`,{
        method: 'GET',
        headers:
        {
            'Content-Type':'application/json',
            'Authorization':`${tok}`
        }

    }
    )
    const data=re.json()
    console.log(data)
    })
    
    async function logoutuser()
    {
        let user={
            "User":sessionStorage.getItem("User"),
            "Token":$tok
            
        }
        fetch(`http://localhost:8000/logout`,{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify(user)
        }
        )
        .then(response =>
            response.json())
        .then(data => {
            console.log("Data",data)
            loggedin.set(false)
            sessionStorage.removeItem("User")
        sessionStorage.removeItem("Valid")
        
        })
       
    }
</script>
<style>
    .cont
    {
        background-color:gold;
        height: 50%;
        width: 50%;
        margin: auto;
        display:block;
        align-items: center;
        justify-content: center;
        font-size: 90%;
    }
</style>
<div class="cont">
    <button on:click={logoutuser}>Logout</button>
    <center>
    <div class="cont-interfaces" >
        <h3>
        Interfaces
        </h3>
    </div>
    <div class="cont-neighbors">
        <h3>Neighbors</h3>
    </div>
    <div  class='cont-advertised'>
        <h3>Advertised Routes</h3>
    </div>
    <div class='cont-bgp'>
        <h3>BGP State</h3></div>
    <div class='cont-routingtable'>
        <h3>Routing Table</h3>
        </div>
        </center>
</div>