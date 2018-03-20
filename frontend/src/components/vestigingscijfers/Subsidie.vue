<template>
  <div>
    <table v-if="allSubsidies.length" class="table table-sm table-striped table-bordered">
      <tbody>
        <tr v-for="entry in allSubsidies" :key="entry.naam">
          <td>
            {{entry[0]}}
          </td>
          <td>
            {{entry[1] ? entry[1] : 'Nee'}}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { getAllSubsidies } from '@/services/subsidiereader'

export default {
  props: [
    'id'
  ],
  data () {
    return {
      'allSubsidies': []
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.id) {
        this.allSubsidies = await getAllSubsidies(2017, this.id)
      }
    }
  },
  watch: {
    id (to, from) {
      this.getData()
    }
  }
}

</script>

<style scoped>
</style>
