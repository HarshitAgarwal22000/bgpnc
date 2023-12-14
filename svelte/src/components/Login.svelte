<style>
.Logincard
{
    background-color: azure;
    width: 40%;
    height: 50%;
    align-items: center;
    justify-content: center;
    display:block;
    margin: auto;
    padding: 1%;
    
}
.warning
{
    width: 50%;
    margin-top: 1%;
    color: red;
    background-color:rgb(191, 169, 169)}
</style>
<script context="module">
  import {writable} from 'svelte/store'
  export let loggedin=writable(false);
  export let tok=writable(null);
</script>
<script>
    import { debug, tick } from "svelte/internal";
  
    import {navigate} from 'svelte-routing'
    import {jwtDecode} from 'jwt-decode'

let password;
let username;
let submit;
let warnin;
let inputg=false;
async function checkuse()
{
    await tick();
    console.log(username.value)
    const rege=new RegExp('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    if (rege.test(username.value)==true)
    {
        warnin=false;
        console.log(warnin)
        return true

    }
    else
    {
        warnin=true;
        console.log(warnin)
        return false
    }
    

}
async function checkin()
{
    await tick()
    if(username.value =="" || password.value =="")
    {
        inputg=false;
    }
    else
    {
        inputg=true;
    }
}
async function submitBack()
{
    await tick();
    let passVal=password.value;
    let userVal=username.value;
    let cred={
        enPass:passVal,
        RouterID:userVal
    }
    console.log(passVal)
    let response=await fetch ("http://localhost:8000/login",
    {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*"
        },
        body:JSON.stringify({cred})
    }
    )
    console.log("Resposne",response);
    let data=await response.json()
    let responsedata=JSON.stringify(data)
    if(response.ok)
    {
        console.log("User validated")
        sessionStorage.setItem("Valid",data.Auth)
        tok.set(data.Auth)
        sessionStorage.setItem("User",userVal)
        loggedin.set(true)
        let dec=jwtDecode(data.Auth)
        console.log(dec)
        await tick()
        
    }

    


}

</script>

<div class="Logincard" >
    <center>
 
    <h3>Login jn</h3>
    <h4>Router ID</h4>
    <input bind:this={username} on:blur={checkuse} on:input={checkin}>
    {#if warnin ==true }
    <div class='warning'>Incorrect Router ID</div>
    {/if}
    <h5>Password</h5>
    <input bind:this={password} on:input={checkin}>
{#if inputg == true}
    <button bind:this={submit} on:click={submitBack}>Submit</button>
{/if}
   </center>

</div>

