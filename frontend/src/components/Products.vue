<script setup>
  

    const prep = defineProps(['product']);

</script>
<template>
    <tr>
        <td>{{prep.product.name}}</td>
        <td>{{prep.product.price}}</td>
        <td>
            <button class="btn btn-primary">Edit</button>
            <button class="btn btn-danger">Delete</button>
        </td>
    </tr>
</template> 