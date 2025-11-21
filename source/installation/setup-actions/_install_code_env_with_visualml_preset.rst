Install code env with Visual ML preset
--------------------------------------

This setup action installs a code environment with the Visual Machine Learning and Visual Time series forecasting preset.

Enable **Install GPU-based preset** to install the GPU-compatible packages. Otherwise, the CPU packages are installed.

Leaving **Allow in-place update** enabled means that if there is a newer version of the preset the next time the setup action runs, and it is compatible with the previously installed code environment, said code environment is updated in place. Otherwise, a new code environment is created with the updated preset.
