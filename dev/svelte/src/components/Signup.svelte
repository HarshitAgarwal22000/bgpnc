<script context='module'>
import {writable} from 'svelte/store'
export let signedin=writable(false);
</script>
<script>
    
    import { tick } from "svelte";
   import {tok} from './Login.svelte'
let router;
let password;
let asn;

async function sub()
{

    await tick();
    let dat={
    "Password":password,
    "Asn":asn
}
    let resp=await fetch(`http://localhost:8000/signup/${router}`,
    {
    method:'POST',
    headers:{
        'Content-Type':'application/json'
    },
    body:JSON.stringify(dat)
}
    )
    let data=await resp.json();
    signedin.set(True)
    console.log(data);
    sessionStorage.setItem("Valid",data.Auth)
    sessionStorage.setItem("User",router)
    tok.set(data.Auth)
    await tick()
    
}


</script>
<style>

</style>
<div>
    <p>Signup</p>
    <p>RouterID</p>
    <input type="text" bind:value={router}>
    <p>Password</p>
    <input bind:value={password}>
    <p>ASN</p>
    <input type="number" bind:value={asn}>
    <button on:click={sub}>Submit</button>
</div>