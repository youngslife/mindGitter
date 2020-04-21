const state = {
  selectedChan: null
};

const getters = {
  getSelectedChan: state => state.selectedChan
};

const mutations = {
  setSelectedChan: (state, channel) => (state.selectedChan = channel)
};

const actions = {};

export default {
  state,
  getters,
  mutations,
  actions
};
