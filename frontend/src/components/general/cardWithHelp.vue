<template>
  <div ref="card" class="card std-height">
    <h5 class="card-header">{{this.title}}</h5>
    <button v-show="this.helpText !== undefined" class="help-button" @click="showHelp = !showHelp">
      <img class="ams-header__logo" src="../../../static/question-mark-icon.svg" height="24px">
    </button>
    <div class="card-block">
      <slot></slot>
      <div v-show="this.showHelp" class="help-overlay">
        <div class="help-content">
          <h6 v-show="this.helpTitle">{{this.helpTitle}}</h6>
          <p>{{this.helpBody}}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'title',
    'helpText'
  ],
  data () {
    return {
      showHelp: false,
      helpTitle: this.helpText && this.helpText.title,
      helpBody: this.helpText && this.helpText.body
    }
  }
}
</script>

<style lang="scss">
  .card {
    border-radius: 0 !important;

    &-header {
      min-height: 49px;
    }

    &-block {
      padding: 10px;
    }

    & button {
      width: 25px;
      height: 25px;
      position: absolute;
      top: 12px;
      right: 12px;
      border: solid 1px #ccc;

      img {
        margin-left: -7px;
        margin-top: -4px;
        width: 24px;
        height: 24px;
      }

      &:hover, &:active {
        background-color: #ccc;
        border-color: #000 !important;
        color: #000 !important;
        outline: none;
        cursor: pointer;

        svg path {
          fill: #000;
        }
      }

      &:focus {
        outline: none;
      }
    }

    $padding: 10px;

    .help-overlay {
      position: absolute;
      left: 0;
      top: 49px;
      right: 0;
      bottom: 0;
      background-color: white;
    }
    .help-content {
      position: absolute;
      left: 10px;
      top: 10px;
      right: 10px;
      bottom: 10px;
      padding: 10px;
      overflow-x: hidden;
      overflow-y: auto;
      background-color: #f7f7f7;
      border: 1px solid #d6d6d6;
      border-radius: 2px;

      p {
        margin-bottom: 0;
      }
    }
  }
</style>
